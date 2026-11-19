import copy
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

import yaml

from validate_work_queue import InvalidQueue, Snapshot, select_candidate, validate


TASK_ID = "FEAT-0001"
PRD = "features/fixture/PRD.md"
TECH = "features/fixture/TECH_SPEC.md"
REPO = "pby1360/fitlog-v2-web"
APPROVAL = "https://example.invalid/approved-fixture"
BACKLOG = "# Fixture backlog\n\n## P1\n\n| FEAT-0001 Fixture | criteria |\n| FEAT-0002 Fixture | criteria |\n"
TASKS = "# Fixture tasks\n\n### FEAT-0001\n\n| 작업 상태 | `APPROVED` |\n\n### V1-04\n\n| 작업 상태 | `DONE` |\n"
PRD_CONTENT = "# Fixture PRD\n\n| 문서 상태 | 확정 |\n\n## 수용 기준\n\n- Fixture behavior.\n"
TECH_CONTENT = "# Fixture Tech Spec\n\n| 문서 상태 | 확정 |\n\n## 테스트 계획\n\n- Fixture test.\n"


class WorkQueueTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.write("status/BACKLOG.md", BACKLOG)
        self.write("status/TASKS.md", TASKS)
        self.write(PRD, PRD_CONTENT)
        self.write(TECH, TECH_CONTENT)
        self.commit("Confirmed specifications")
        self.sha = self.git("rev-parse", "HEAD").strip()
        self.entry = {
            "task_id": TASK_ID, "backlog_ref": "status/BACKLOG.md#p1", "prd_ref": PRD, "tech_spec_ref": TECH,
            "repositories": [REPO], "priority": "P1", "auto_development_allowed": True,
            "approval_ref": APPROVAL, "approved_spec_sha": self.sha, "depends_on": ["V1-04"], "state": "READY",
        }

    def git(self, *args):
        return subprocess.check_output(["git", "-C", self.root, *args], encoding="utf-8")

    def write(self, path, text):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")

    def commit(self, title):
        self.git("add", ".")
        self.git("commit", "-qm", title)

    def verify(self, entries=None, raw=None):
        if raw is None:
            tasks = [self.entry] if entries is None else entries
            raw = yaml.safe_dump({"schema_version": 1, "tasks": tasks})
        self.write("status/WORK_QUEUE.yaml", raw)
        self.commit("Fixture queue")
        return validate(Snapshot(self.root, "HEAD"))

    def approval(self, task_id=TASK_ID):
        return (task_id, APPROVAL, self.sha, (REPO,))

    def pick(self, entries, statuses, **overrides):
        inputs = {"verified_approvals": {self.approval()}, "activity_verified_idle": True, "execution_available": True}
        return select_candidate(entries, statuses, **(inputs | overrides))

    def test_empty_queue(self):
        self.assertEqual(self.verify(entries=[])[0], [])

    def test_ready_uses_approved_unchanged_specs(self):
        entries, statuses = self.verify()
        self.assertEqual(self.pick(entries, statuses), TASK_ID)

    def test_supports_existing_hyphenated_task_prefixes(self):
        self.write("status/TASKS.md", TASKS + "\n### DEV-LOOP-01\n\n| 작업 상태 | `DONE` |\n")
        self.entry["depends_on"] = ["DEV-LOOP-01"]
        entries, statuses = self.verify()
        self.assertEqual(self.pick(entries, statuses), TASK_ID)

    def test_rejects_duplicate_yaml_keys(self):
        with self.assertRaisesRegex(InvalidQueue, "unique strings"):
            self.verify(raw="schema_version: 1\ntasks: []\ntasks: []\n")

    def test_rejects_duplicate_queue_ids(self):
        with self.assertRaisesRegex(InvalidQueue, "Duplicate WORK_QUEUE"):
            self.verify(entries=[self.entry, copy.deepcopy(self.entry)])

    def test_rejects_duplicate_status_ids(self):
        self.write("status/TASKS.md", TASKS + TASKS)
        with self.assertRaisesRegex(InvalidQueue, "Duplicate or invalid TASKS"):
            self.verify()

    def test_rejects_duplicate_backlog_ids(self):
        self.write("status/BACKLOG.md", BACKLOG + BACKLOG)
        with self.assertRaisesRegex(InvalidQueue, "Duplicate BACKLOG"):
            self.verify()

    def test_ready_requires_approval_evidence(self):
        self.entry["approval_ref"] = None
        with self.assertRaisesRegex(InvalidQueue, "schema mismatch"):
            self.verify()

    def test_ready_rejects_a_task_still_waiting_for_approval(self):
        self.write("status/TASKS.md", TASKS.replace("`APPROVED`", "`PROPOSED`"))
        with self.assertRaisesRegex(InvalidQueue, "requires an approved TASKS record"):
            self.verify()

    def test_ready_requires_automatic_development_permission(self):
        self.entry["auto_development_allowed"] = False
        with self.assertRaisesRegex(InvalidQueue, "schema mismatch"):
            self.verify()

    def test_rejects_yaml_11_boolean_alias(self):
        raw = yaml.safe_dump({"schema_version": 1, "tasks": [self.entry]}).replace(": true", ": yes")
        with self.assertRaisesRegex(InvalidQueue, "schema mismatch"):
            self.verify(raw=raw)

    def test_waiting_can_be_recorded_without_automatic_approval(self):
        self.entry.update(state="WAITING", auto_development_allowed=False, approval_ref=None, approved_spec_sha=None)
        entries, statuses = self.verify()
        self.assertIsNone(self.pick(entries, statuses))

    def test_ready_requires_done_dependency(self):
        self.write("status/TASKS.md", TASKS.replace("`DONE`", "`PR_OPEN`"))
        with self.assertRaisesRegex(InvalidQueue, "Dependencies not DONE"):
            self.verify()

    def test_rejects_self_dependency(self):
        self.entry["depends_on"] = [TASK_ID]
        with self.assertRaisesRegex(InvalidQueue, "Invalid dependency"):
            self.verify()

    def test_approved_spec_content_change_blocks_candidate(self):
        self.write(PRD, PRD_CONTENT + "\n- Changed acceptance criteria.\n")
        with self.assertRaisesRegex(InvalidQueue, "Approved specification changed"):
            self.verify()

    def test_ready_requires_acceptance_criteria(self):
        self.write(PRD, PRD_CONTENT.replace("## 수용 기준", "## 개요"))
        self.commit("Missing acceptance criteria")
        self.entry["approved_spec_sha"] = self.git("rev-parse", "HEAD").strip()
        with self.assertRaisesRegex(InvalidQueue, "수용 기준"):
            self.verify()

    def test_rejects_missing_spec_link(self):
        self.entry.update(prd_ref="features/missing/PRD.md", tech_spec_ref="features/missing/TECH_SPEC.md")
        with self.assertRaisesRegex(InvalidQueue, "could not verify"):
            self.verify()

    def test_backlog_priority_and_anchor_have_to_match(self):
        self.entry["backlog_ref"] = "status/BACKLOG.md#p0"
        with self.assertRaisesRegex(InvalidQueue, "BACKLOG Task ID, section, or priority"):
            self.verify()

    def test_verified_approval_must_bind_the_exact_sha(self):
        self.write("README.md", "Unrelated new commit")
        self.commit("Change other docs")
        self.entry["approved_spec_sha"] = self.git("rev-parse", "HEAD").strip()
        entries, statuses = self.verify()
        self.assertIsNone(self.pick(entries, statuses))

    def test_claimed_or_active_task_blocks_selection(self):
        entries, statuses = self.verify()
        for current in ("STARTING", "IN_PROGRESS", "PR_OPEN"):
            with self.subTest(current=current):
                self.assertIsNone(self.pick(entries, statuses | {TASK_ID: current}))
                self.assertIsNone(self.pick(entries, statuses | {"FEAT-0002": current}))

    def test_unavailable_cloud_or_untrusted_activity_blocks_selection(self):
        entries, statuses = self.verify()
        self.assertIsNone(self.pick(entries, statuses, execution_available=False))
        self.assertIsNone(self.pick(entries, statuses, activity_verified_idle=False))
        self.assertIsNone(self.pick(entries, statuses, verified_approvals=set()))

    def test_selection_uses_priority_then_id(self):
        other_id = "FEAT-0002"
        other_entry = dict(self.entry, task_id=other_id)
        self.write("status/TASKS.md", TASKS + "\n### FEAT-0002\n\n| 작업 상태 | `APPROVED` |\n")
        entries, statuses = self.verify(entries=[other_entry, self.entry])
        approvals = {self.approval(), self.approval(other_id)}
        self.assertEqual(self.pick(entries, statuses, verified_approvals=approvals), TASK_ID)
        self.write("status/BACKLOG.md", BACKLOG.replace("| FEAT-0002", "## P0\n\n| FEAT-0002"))
        other_entry.update(priority="P0", backlog_ref="status/BACKLOG.md#p0")
        entries, statuses = self.verify(entries=[self.entry, other_entry])
        self.assertEqual(self.pick(entries, statuses, verified_approvals=approvals), other_id)
