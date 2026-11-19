"""Validate a committed FitLog queue snapshot without changing state or starting work."""

import argparse
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
TASK_ID = r"(?:[A-Z][A-Z0-9]*-)+[0-9]{2,}(?:-[A-Z0-9]+)*"
TASK_STATES = {"TODO", "PROPOSED", "APPROVED", "STARTING", "IN_PROGRESS", "PR_OPEN", "BLOCKED", "DONE", "CANCELLED"}
ACTIVE = {"STARTING", "IN_PROGRESS", "PR_OPEN"}
SPEC_STATUS = re.compile(r"^\| 문서 상태 \| ([^|]+?) \|$", re.MULTILINE)
SPEC_SECTIONS = {"PRD.md": "수용 기준", "TECH_SPEC.md": "테스트 계획"}


class InvalidQueue(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    yaml_implicit_resolvers = {
        key: [(tag, pattern) for tag, pattern in rules if tag != "tag:yaml.org,2002:bool"]
        for key, rules in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        seen = set()
        for key, _ in node.value:
            key = self.construct_object(key, deep=deep)
            if not isinstance(key, str) or key in seen:
                raise InvalidQueue("YAML keys must be unique strings.")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


UniqueKeyLoader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(true|false)$"), ["t", "f"])


class Snapshot:
    def __init__(self, root, revision):
        self.root = root
        self.commit = self.git("rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}").strip()

    def git(self, *args):
        result = subprocess.run(["git", "-C", self.root, *args], capture_output=True)
        if result.returncode != 0:
            raise InvalidQueue(f"Git could not verify {' '.join(args)}.")
        return result.stdout.decode("utf-8")

    def read(self, path, commit=None):
        return self.git("show", f"{commit or self.commit}:{path}")


def backlog_priorities(markdown):
    priorities = {}
    priority = None
    for line in markdown.splitlines():
        if line.startswith("## "):
            section = line[3:]
            priority = section if section in {"P0", "P1", "P2", "P3"} else None
        match = re.match(rf"\| `?({TASK_ID})`?(?:\s|\|)", line)
        if match and priority:
            task_id = match[1]
            if task_id in priorities:
                raise InvalidQueue(f"Duplicate BACKLOG Task ID: {task_id}.")
            priorities[task_id] = priority
    return priorities


def task_statuses(markdown):
    sections = re.split(rf"^### ({TASK_ID})\s*$", markdown, flags=re.MULTILINE)
    statuses = {}
    for task_id, section in zip(sections[1::2], sections[2::2]):
        state, *duplicates = re.findall(r"^\| 작업 상태 \| `([A-Z_]+)` \|$", section, re.MULTILINE) or [None]
        if task_id in statuses or duplicates or state not in TASK_STATES:
            raise InvalidQueue(f"Duplicate or invalid TASKS status: {task_id}.")
        statuses[task_id] = state
    return statuses


def validate(snapshot):
    queue = yaml.load(snapshot.read("status/WORK_QUEUE.yaml"), Loader=UniqueKeyLoader)
    schema = json.loads((ROOT / "status/WORK_QUEUE.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    error = next(Draft202012Validator(schema).iter_errors(queue), None)
    if error:
        location = ".".join(map(str, error.absolute_path)) or "queue"
        raise InvalidQueue(f"YAML schema mismatch at {location}: {error.validator}.")

    priorities = backlog_priorities(snapshot.read("status/BACKLOG.md"))
    statuses = task_statuses(snapshot.read("status/TASKS.md"))
    entries = queue["tasks"]
    seen = set()
    for entry in entries:
        task_id = entry["task_id"]
        if task_id in seen:
            raise InvalidQueue(f"Duplicate WORK_QUEUE Task ID: {task_id}.")
        seen.add(task_id)
    for entry in entries:
        validate_entry(snapshot, entry, priorities, statuses)
    return entries, statuses


def validate_entry(snapshot, entry, priorities, statuses):
    task_id = entry["task_id"]
    priority = priorities.get(task_id)
    if not priority or priority != entry["priority"] or entry["backlog_ref"] != f"status/BACKLOG.md#{priority.lower()}":
        raise InvalidQueue(f"BACKLOG Task ID, section, or priority does not match: {task_id}.")

    paths = (entry["prd_ref"], entry["tech_spec_ref"])
    if len({Path(path).parent for path in paths}) != 1:
        raise InvalidQueue(f"PRD and Tech Spec must be for the same feature: {task_id}.")
    documents = {path: snapshot.read(path) for path in paths}

    for dependency in entry["depends_on"]:
        if dependency == task_id or (dependency not in statuses and dependency not in priorities):
            raise InvalidQueue(f"Invalid dependency {dependency} for {task_id}.")
    if entry["state"] != "READY":
        return

    if statuses.get(task_id) in {None, "TODO", "PROPOSED"}:
        raise InvalidQueue(f"READY requires an approved TASKS record: {task_id}.")
    approval = urlsplit(entry["approval_ref"])
    if not approval.hostname or approval.username or approval.password:
        raise InvalidQueue(f"Invalid approval reference: {task_id}.")
    if not all(statuses.get(dep) == "DONE" for dep in entry["depends_on"]):
        raise InvalidQueue(f"Dependencies not DONE: {task_id}.")
    sha = entry["approved_spec_sha"]
    snapshot.git("merge-base", "--is-ancestor", sha, snapshot.commit)
    for path, current in documents.items():
        if current != snapshot.read(path, sha):
            raise InvalidQueue(f"Approved specification changed: {path} ({task_id}).")
        if SPEC_STATUS.findall(current) != ["확정"]:
            raise InvalidQueue(f"Specification is not confirmed: {path} ({task_id}).")
        heading = SPEC_SECTIONS[Path(path).name]
        section = re.search(rf"^## {heading}\s*\n(.*?)(?=^## |\Z)", current, re.MULTILINE | re.DOTALL)
        if not section or not section[1].strip():
            raise InvalidQueue(f"Specification needs a {heading} section: {path} ({task_id}).")


def select_candidate(entries, statuses, *, verified_approvals, activity_verified_idle, execution_available):
    """Return one candidate ID from validated inputs, never a claim or permission to launch."""
    if not activity_verified_idle or not execution_available or ACTIVE.intersection(statuses.values()):
        return None
    candidates = []
    for entry in entries:
        task_id = entry["task_id"]
        approval = (task_id, entry["approval_ref"], entry["approved_spec_sha"], tuple(sorted(entry["repositories"])))
        if entry["state"] == "READY" and statuses.get(task_id) == "APPROVED" and approval in verified_approvals:
            candidates.append((entry["priority"], task_id))
    return min(candidates)[1] if candidates else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("revision", nargs="?", default="HEAD", help="committed snapshot to validate")
    try:
        entries, _ = validate(Snapshot(ROOT, parser.parse_args().revision))
        print(f"Valid work queue: {len(entries)} entries. No state changes or tasks started.")
    except (ValueError, yaml.YAMLError) as error:
        parser.exit(1, f"Invalid work queue: {error}\n")
