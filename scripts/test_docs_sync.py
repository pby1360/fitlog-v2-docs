"""Workflow scenarios without credentials, GitHub mutations, or deployment."""
import base64
import random
import string
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError

from docs_sync import Blocked, DOCS, GitHub, METADATA, synchronize


CODE = "pby1360/fitlog-v2-web"
CODE_BASE = "1" * 40
CODE_HEAD = "2" * 40
CODE_MERGE = "3" * 40
DOCS_BASE = "4" * 40
DOCS_HEAD = "5" * 40
CODE_TREE = "6" * 40
CODE_BLOB = "7" * 40
DOCS_TREE = "a" * 40
CODE_PATH = "src/pages/history/page.tsx"
HISTORY = "history/2026-11-19.md"


class FixtureGitHub:
    def __init__(self):
        self.responses = {}
        self.writes = []
        self.files = {}

    def request(self, path, method="GET", body=None):
        if method == "PUT":
            self.writes.append((path, body))
            self.responses[f"repos/{DOCS}/pulls/12"]["merged"] = True
            return {"merged": True, "sha": DOCS_HEAD}
        return self.responses[path]

    def pr_files(self, repo, number, count):
        files = self.files[repo, number]
        if len(files) != count:
            raise AssertionError("Fixture PR files mismatch")
        return files


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.configure_fixture(CODE, CODE_PATH)

    def configure_fixture(self, repository, code_path):
        self.docs = FixtureGitHub()
        self.code = FixtureGitHub()
        self.event = {"code_repository": repository, "code_number": 40, "merge_sha": CODE_MERGE}
        self.source = {
            "merged": True, "merge_commit_sha": CODE_MERGE, "changed_files": 1,
            "title": "Implement calendar fix", "body": "Linked Docs PR: #12",
            "base": {"ref": "main", "repo": {"full_name": repository}}, "head": {"sha": CODE_HEAD},
        }
        self.merge_message = {
            "message": "Merge calendar implementation\n\nDocs-Sync-Kind: implementation\n"
                       f"Docs-Sync-PR: 12\nDocs-Sync-Head: {DOCS_HEAD}",
            "tree": {"sha": CODE_TREE},
        }
        self.code.responses.update({
            f"repos/{repository}/pulls/40": self.source,
            f"repos/{repository}/commits/{CODE_MERGE}": {
                "parents": [{"sha": CODE_BASE}, {"sha": CODE_HEAD}], "commit": self.merge_message,
            },
            f"repos/{repository}/compare/{CODE_BASE}...{CODE_BASE}?per_page=1": {"status": "identical"},
            f"repos/{repository}/compare/{CODE_BASE}...{CODE_HEAD}?per_page=1": {"status": "ahead"},
            f"repos/{repository}/git/ref/heads/main": {"object": {"sha": CODE_MERGE}},
            f"repos/{repository}/compare/{CODE_MERGE}...{CODE_MERGE}?per_page=1": {"status": "identical"},
            f"repos/{repository}/git/trees/{CODE_TREE}?recursive=1": {
                "truncated": False, "tree": [{"path": code_path, "type": "blob", "sha": CODE_BLOB}],
            },
        })
        self.code.files[repository, 40] = [{"filename": code_path, "status": "modified", "sha": CODE_BLOB}]

        self.proposal = {
            "number": 12, "state": "open", "draft": False, "merged": False, "changed_files": 3,
            "base": {"ref": "main", "repo": {"full_name": DOCS}},
            "head": {"sha": DOCS_HEAD, "ref": f"docs/sync/{repository.split('/')[-1]}-40", "repo": {"full_name": DOCS}},
            "body": f"Docs-Sync-Source: {repository}#40\nDocs-Sync-Base: {CODE_BASE}",
        }
        self.docs.responses.update({
            f"repos/{DOCS}/pulls/12": self.proposal,
            f"repos/{DOCS}/git/ref/heads/main": {"object": {"sha": DOCS_BASE}},
            f"repos/{DOCS}/compare/{DOCS_BASE}...{DOCS_HEAD}?per_page=1": {"status": "ahead"},
            f"repos/{DOCS}/git/commits/{DOCS_HEAD}": {"tree": {"sha": DOCS_TREE}},
            f"repos/{DOCS}/git/trees/{DOCS_TREE}?recursive=1": {"truncated": False, "tree": []},
        })
        self.docs.files[DOCS, 12] = []
        self.valid_markdown = (
            "# 구현 동기화\n\n## 변경 사항\n\n"
            f"[코드](https://github.com/{repository}/blob/{CODE_HEAD}/{code_path})\n\n"
            + "\n".join(f"| {label} | Fixture |" for label in METADATA)
        )
        for index, path in enumerate(("status/CURRENT_STATUS.md", "status/BACKLOG.md", HISTORY)):
            sha = str(index + 1) * 40
            self.docs.files[DOCS, 12].append({"filename": path, "status": "modified", "sha": sha})
            self.docs.responses[f"repos/{DOCS}/git/trees/{DOCS_TREE}?recursive=1"]["tree"].append(
                {"path": path, "sha": sha, "type": "blob", "mode": "100644"}
            )
            self.set_blob(sha, self.valid_markdown)

    def set_blob(self, sha, content):
        data = content.encode("utf-8")
        self.docs.responses[f"repos/{DOCS}/git/blobs/{sha}"] = {
            "content": base64.b64encode(data).decode(), "size": len(data), "encoding": "base64",
        }

    def run_sync(self):
        return synchronize(self.docs, self.code, self.event)

    def assert_blocked(self, reason):
        with self.assertRaisesRegex(Blocked, reason):
            self.run_sync()
        self.assertEqual(self.docs.writes, [])

    def test_unmerged_code_cannot_merge_docs(self):
        self.source["merged"] = False
        self.assert_blocked("has not merged")

    def test_merged_code_and_valid_docs_merge_once_at_the_expected_sha(self):
        self.assertIn("Docs PR #12 merged", self.run_sync())
        self.assertEqual(len(self.docs.writes), 1)
        self.assertEqual(self.docs.writes[0][1]["sha"], DOCS_HEAD)
        self.assertEqual(self.code.writes, [])

    def test_server_event_merges_only_the_approved_docs_head(self):
        self.configure_fixture("pby1360/fitlog-v2-server", "src/main/java/fitlog/Workout.java")
        self.assertIn("Docs PR #12 merged", self.run_sync())
        self.assertEqual(len(self.docs.writes), 1)
        self.assertEqual(self.docs.writes[0][1]["sha"], DOCS_HEAD)
        self.assertEqual(self.code.writes, [])

    def test_event_without_authorization_does_not_write(self):
        self.merge_message["message"] = "Merge without Docs authorization"
        self.assert_blocked("Docs-Sync-Kind")

    def test_missing_pull_request_or_denied_api_read_does_not_write(self):
        for status in (401, 403, 404):
            with self.subTest(status=status):
                code = GitHub("offline-test")
                code.opener = Mock()
                code.opener.open.side_effect = HTTPError(
                    "https://api.github.com/offline-test", status, "Fixture error", None, None,
                )
                with self.assertRaisesRegex(Blocked, rf"GitHub rejected GET \({status}\)"):
                    synchronize(self.docs, code, self.event)
                code.opener.open.assert_called_once()
                self.assertEqual(self.docs.writes, [])

    def test_previously_merged_docs_pr_exits_without_writes(self):
        self.proposal["merged"] = True
        self.assertIn("already merged", self.run_sync())
        self.assertEqual(self.docs.writes, [])
        self.assertEqual(self.code.writes, [])

    def test_main_moving_after_document_validation_does_not_write(self):
        request = self.docs.request
        base_path = f"repos/{DOCS}/git/ref/heads/main"
        bases = iter((DOCS_BASE, "9" * 40))

        def change_base_after_first_read(path, method="GET", body=None):
            if path == base_path and method == "GET":
                return {"object": {"sha": next(bases)}}
            return request(path, method, body)

        with patch.object(self.docs, "request", side_effect=change_base_after_first_read):
            self.assert_blocked("Docs main moved during validation")

    def test_broken_relative_link_blocks_merge(self):
        self.set_blob("1" * 40, self.valid_markdown + "\n[없는 문서](missing.md)")
        self.assert_blocked("Broken relative")

    def test_broken_anchor_blocks_merge(self):
        self.set_blob("1" * 40, self.valid_markdown + "\n[없는 제목](BACKLOG.md#없는-제목)")
        self.assert_blocked("Broken Markdown heading")

    def test_valid_relative_heading_link_passes(self):
        self.set_blob("1" * 40, self.valid_markdown + "\n[백로그 변경 사항](BACKLOG.md#변경-사항)")
        self.assertIn("merged", self.run_sync())

    def test_raw_html_does_not_bypass_link_validation(self):
        self.set_blob("1" * 40, self.valid_markdown + '\n\n<a href="missing.md">없는 문서</a>')
        self.assert_blocked("Raw HTML")

    def test_missing_required_metadata_blocks_merge(self):
        self.set_blob("2" * 40, "# 불완전 문서")
        self.assert_blocked("tracking metadata")

    def test_secret_blocks_merge_even_with_a_pr_supplied_allowlist_comment(self):
        synthetic = "ghp_" + "".join(random.Random(27).sample(string.ascii_letters + string.digits, 36))
        self.set_blob("1" * 40, self.valid_markdown + "\nsynthetic = " + synthetic + " # pragma: allowlist secret")
        self.assert_blocked("potential secret")

    def test_duplicate_event_does_not_merge_or_write_again(self):
        self.run_sync()
        self.assertIn("already merged", self.run_sync())
        self.assertEqual(len(self.docs.writes), 1)

    def test_missing_dated_history_blocks_merge(self):
        self.docs.files[DOCS, 12].pop()
        self.proposal["changed_files"] -= 1
        self.assert_blocked("one dated history")

    def test_product_scope_requires_manual_approval(self):
        self.docs.files[DOCS, 12].append({"filename": "product/REQUIREMENTS.md", "status": "modified"})
        self.proposal["changed_files"] += 1
        self.assert_blocked("manual Docs approval")

    def test_decision_file_is_rejected_even_in_an_otherwise_valid_pr(self):
        self.docs.files[DOCS, 12].append({"filename": "decisions/0001-policy.md", "status": "added"})
        self.proposal["changed_files"] += 1
        self.assert_blocked("manual Docs approval")

    def test_a_non_implementation_approval_cannot_merge(self):
        self.merge_message["message"] = self.merge_message["message"].replace("implementation", "policy")
        self.assert_blocked("Docs-Sync-Kind")

    def test_authorization_fields_cannot_come_from_the_pr_description(self):
        self.source["body"] = self.merge_message["message"]
        self.assert_blocked("reserved merge authorization")

    def test_unapproved_doc_head_cannot_merge(self):
        self.proposal["head"]["sha"] = "9" * 40
        self.assert_blocked("authorized snapshot")

    def test_fork_head_cannot_merge(self):
        self.proposal["head"]["repo"]["full_name"] = "someone/fitlog-v2-docs"
        self.assert_blocked("authorized snapshot")

    def test_unrelated_code_evidence_blocks_merge(self):
        self.set_blob("1" * 40, self.valid_markdown.replace(CODE_PATH, "src/unrelated.ts"))
        self.assert_blocked("commit-pinned link")

    def test_pre_merge_evidence_must_match_the_final_merged_blob(self):
        snapshot = self.code.responses[f"repos/{CODE}/git/trees/{CODE_TREE}?recursive=1"]
        snapshot["tree"][0]["sha"] = "8" * 40
        self.assert_blocked("commit-pinned link")

    def test_moved_docs_base_cannot_merge(self):
        self.docs.responses[f"repos/{DOCS}/compare/{DOCS_BASE}...{DOCS_HEAD}?per_page=1"] = {
            "status": "diverged",
        }
        self.assert_blocked("current main")
