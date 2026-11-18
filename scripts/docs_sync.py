"""Validate a docs-sync event using GitHub metadata and inert Markdown blobs."""
import base64
from collections import Counter
import json
import os
from pathlib import Path
import posixpath
import re
import sys
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.parse import unquote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings
from markdown_it import MarkdownIt


DOCS = "pby1360/fitlog-v2-docs"
CODE_REPOS = {"pby1360/fitlog-v2-server", "pby1360/fitlog-v2-web"}
REQUIRED = {"status/CURRENT_STATUS.md", "status/BACKLOG.md"}
HISTORY = r"history/\d{4}-\d{2}-\d{2}\.md"
IMPLEMENTATION_DOC = re.compile(
    r"status/(?:CURRENT_STATUS|BACKLOG)\.md|features/[a-z0-9-]+/TECH_SPEC\.md|"
    r"architecture/(?:SYSTEM_OVERVIEW|FRONTEND|BACKEND|DATA_MODEL)\.md|api/README\.md|" + HISTORY
)
METADATA = ("문서 상태", "원본 출처", "관련 기능 또는 Issue", "최종 검증일", "관련 설계")
SHA = r"[0-9a-f]{40}"
AUTHORIZATION_FIELD = re.compile(r"Docs-Sync-(?:Kind|PR|Head):", re.IGNORECASE)
MARKDOWN = MarkdownIt("commonmark").enable("table")
FILE_LIMIT = 256 * 1024


class Blocked(Exception):
    """The requested change could not be verified."""


def require(condition, message):
    if not condition:
        raise Blocked(message)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class GitHub:
    def __init__(self, token):
        self.token = token
        self.opener = build_opener(NoRedirect)

    def request(self, path, method="GET", body=None):
        request = Request(
            "https://api.github.com/" + path, method=method,
            headers={"Authorization": "Bearer " + self.token, "Accept": "application/vnd.github+json",
                     "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json"},
            data=json.dumps(body).encode() if body is not None else None,
        )
        try:
            with self.opener.open(request, timeout=20) as response:
                return json.load(response)
        except HTTPError as exc:
            raise Blocked(f"GitHub rejected {method} ({exc.code}).") from None

    def pr_files(self, repo, number, count):
        require(0 < count <= 3000, "PR file count is missing or exceeds the GitHub API limit.")
        files = []
        for page in range(1, (count + 99) // 100 + 1):
            files.extend(self.request(f"repos/{repo}/pulls/{number}/files?per_page=100&page={page}"))
        require(len(files) == count, "PR changed files changed during validation.")
        return files


def field(text, name, pattern):
    matches = re.findall(r"^" + re.escape(name) + r": (.*)$", text or "", re.MULTILINE)
    require(len(matches) == 1 and re.fullmatch(pattern, matches[0]), f"Missing or invalid {name}.")
    return matches[0]


def markdown_tokens(content):
    for token in MARKDOWN.parse(content):
        yield token
        yield from token.children or ()


def github_heading(text):
    return re.sub(r"[^\w\s-]", "", text.strip().lower()).replace(" ", "-")


def heading_ids(content):
    result = set()
    counts = Counter()
    tokens = MARKDOWN.parse(content)
    for index, token in enumerate(tokens[:-1]):
        if token.type == "heading_open":
            inline = tokens[index + 1]
            text = "".join(child.content for child in inline.children or ()
                           if child.type in {"text", "code_inline", "image"})
            slug = github_heading(text)
            suffix = counts[slug]
            while (slug if suffix == 0 else f"{slug}-{suffix}") in result:
                suffix += 1
            counts[slug] = suffix + 1
            result.add(slug if suffix == 0 else f"{slug}-{suffix}")
    return result


def check_links(path, text, tree, read_blob):
    for token in markdown_tokens(text):
        require(token.type not in {"html_block", "html_inline"}, f"Raw HTML in {path} needs manual review.")
        if token.type not in {"link_open", "image"}:
            continue
        target = urlsplit(token.attrGet("href" if token.type == "link_open" else "src") or "")
        if target.scheme == "https" and target.hostname and not target.username and not target.password:
            continue  # External links are syntax-checked without following arbitrary URLs.
        require(not target.scheme and not target.netloc and not target.query,
                f"Use a relative or HTTPS Markdown link in {path}.")
        relative = unquote(target.path)
        destination = posixpath.normpath(posixpath.join(posixpath.dirname(path), relative)) if relative else path
        require(destination in tree, f"Broken relative Markdown link in {path}.")
        if target.fragment and destination.endswith(".md"):
            require(unquote(target.fragment) in heading_ids(read_blob(destination)),
                    f"Broken Markdown heading link in {path}.")


def scan_secrets(changed):
    with TemporaryDirectory() as temp, default_settings() as settings:
        settings.disable_filters("detect_secrets.filters.allowlist.is_line_allowlisted")
        secrets = SecretsCollection()
        for index, content in enumerate(changed.values()):
            path = Path(temp, f"{index}.md")
            path.write_text(content, encoding="utf-8")
            secrets.scan_file(str(path))
        require(not list(secrets), "The sensitive-data scanner found a potential secret.")


def validate_documents(docs, code_files, code_tree, docs_pr, repo, code_head, merge_sha):
    number = docs_pr["number"]
    head = docs_pr["head"]["sha"]
    changed = docs.pr_files(DOCS, number, docs_pr["changed_files"])
    paths = {file["filename"] for file in changed}
    require(len(paths) == len(changed), "Unexpected duplicate docs file.")
    require(REQUIRED <= paths and sum(bool(re.fullmatch(HISTORY, path)) for path in paths) == 1,
            "Implementation sync requires current status, backlog, and one dated history file.")
    require(all(IMPLEMENTATION_DOC.fullmatch(file["filename"]) and file["status"] in {"added", "modified"}
                for file in changed), "This file change needs manual Docs approval.")

    commit = docs.request(f"repos/{DOCS}/git/commits/{head}")
    tree_sha = commit["tree"]["sha"]
    snapshot = docs.request(f"repos/{DOCS}/git/trees/{tree_sha}?recursive=1")
    require(not snapshot["truncated"], "Docs tree is incomplete.")
    tree = {item["path"]: item["sha"] for item in snapshot["tree"]
            if item["type"] == "blob" and item["mode"] == "100644"}
    cache = {}

    def read_blob(path):
        if path not in cache:
            blob = docs.request(f"repos/{DOCS}/git/blobs/{tree[path]}")
            require(blob["size"] <= FILE_LIMIT and blob["encoding"] == "base64",
                    f"Unsupported Markdown file in {path}.")
            cache[path] = base64.b64decode(blob["content"]).decode("utf-8")
        return cache[path]

    sources = set()
    for file in code_files:
        path = file["filename"]
        if file["status"] == "removed" or path not in code_tree:
            continue
        sources.add(f"/{repo}/blob/{merge_sha}/{path}")
        if code_tree[path] == file["sha"]:
            sources.add(f"/{repo}/blob/{code_head}/{path}")
    documents = {}
    for file in changed:
        path = file["filename"]
        require(tree.get(path) == file["sha"], f"Invalid file or snapshot changed in {path}.")
        text = read_blob(path)
        require(all(re.search(r"^\| " + label + r" \| [^|\n]+ \|$", text, re.MULTILINE)
                    for label in METADATA), f"Missing tracking metadata in {path}.")
        require(any(token.type == "heading_open" and token.tag == "h1" for token in markdown_tokens(text)),
                f"Missing top-level heading in {path}.")
        require(not re.search(r"\[\[[^\n]+?\]\]", text), f"Obsidian link in {path}.")
        check_links(path, text, tree, read_blob)
        if path == "status/CURRENT_STATUS.md" or re.fullmatch(HISTORY, path):
            urls = [urlsplit(token.attrGet("href")) for token in markdown_tokens(text)
                    if token.type == "link_open" and token.attrGet("href")]
            require(any(url.scheme == "https" and url.netloc == "github.com" and unquote(url.path) in sources for url in urls),
                    f"Missing a commit-pinned link to a changed code file in {path}.")
        documents[path] = text
    scan_secrets(documents)


def synchronize(docs, code, payload):
    repo = payload.get("code_repository")
    number = payload.get("code_number")
    merge_sha = payload.get("merge_sha")
    require(repo in CODE_REPOS and type(number) is int and number > 0
            and isinstance(merge_sha, str) and re.fullmatch(SHA, merge_sha), "Invalid dispatch payload.")

    source = code.request(f"repos/{repo}/pulls/{number}")
    require(source["merged"] and source["merge_commit_sha"] == merge_sha
            and source["base"]["ref"] == "main" and source["base"]["repo"]["full_name"] == repo,
            "Linked code PR has not merged into the expected main commit.")
    require(not AUTHORIZATION_FIELD.search((source["title"] or "") + "\n" + (source["body"] or "")),
            "The code PR title or body contains reserved merge authorization fields.")
    merge = code.request(f"repos/{repo}/commits/{merge_sha}")
    code_head = source["head"]["sha"]
    parents = merge["parents"]
    require(len(parents) == 2 and parents[1]["sha"] == code_head,
            "Docs auto-merge requires a code merge commit with the approved PR head as its second parent.")
    final_paragraph = merge["commit"]["message"].strip().rsplit("\n\n", 1)[-1]
    field(final_paragraph, "Docs-Sync-Kind", "implementation")
    docs_number = int(field(final_paragraph, "Docs-Sync-PR", r"[1-9]\d*"))
    docs_head = field(final_paragraph, "Docs-Sync-Head", SHA)

    proposal = docs.request(f"repos/{DOCS}/pulls/{docs_number}")
    require(proposal["head"]["sha"] == docs_head and proposal["base"]["ref"] == "main"
            and proposal["base"]["repo"]["full_name"] == DOCS
            and proposal["head"]["repo"]["full_name"] == DOCS
            and proposal["head"]["ref"] == f"docs/sync/{repo.split('/')[1]}-{number}",
            "Docs PR branch or head differs from the authorized snapshot.")
    field(proposal["body"], "Docs-Sync-Source", re.escape(f"{repo}#{number}"))
    source_base = field(proposal["body"], "Docs-Sync-Base", SHA)
    if proposal["merged"]:
        return f"Docs PR #{docs_number} already merged. No changes made."
    require(proposal["state"] == "open" and not proposal["draft"], "Docs PR must be open and ready.")

    for revision in (parents[0]["sha"], code_head):
        comparison = code.request(f"repos/{repo}/compare/{source_base}...{revision}?per_page=1")
        require(comparison["status"] in {"ahead", "identical"}, "Docs source base is outside the merged code history.")

    base_ref = f"repos/{DOCS}/git/ref/heads/main"
    docs_base = docs.request(base_ref)["object"]["sha"]
    comparison = docs.request(f"repos/{DOCS}/compare/{docs_base}...{docs_head}?per_page=1")
    require(comparison["status"] == "ahead", "Docs branch needs the current main as its base.")
    code_main = code.request(f"repos/{repo}/git/ref/heads/main")["object"]["sha"]
    comparison = code.request(f"repos/{repo}/compare/{merge_sha}...{code_main}?per_page=1")
    require(comparison["status"] in {"ahead", "identical"}, "Code merge is outside the current main history.")
    code_files = code.pr_files(repo, number, source["changed_files"])
    code_tree_sha = merge["commit"]["tree"]["sha"]
    snapshot = code.request(f"repos/{repo}/git/trees/{code_tree_sha}?recursive=1")
    require(not snapshot["truncated"], "Merged code tree is incomplete.")
    code_tree = {item["path"]: item["sha"] for item in snapshot["tree"] if item["type"] == "blob"}
    validate_documents(docs, code_files, code_tree, proposal, repo, code_head, merge_sha)

    require(docs.request(base_ref)["object"]["sha"] == docs_base, "Docs main moved during validation.")
    result = docs.request(f"repos/{DOCS}/pulls/{docs_number}/merge", "PUT", {
        "sha": docs_head, "merge_method": "merge", "commit_title": f"Sync docs for {repo}#{number}",
    })
    require(result["merged"], "GitHub did not merge the verified docs PR.")
    return f"Docs PR #{docs_number} merged at {result['sha']}."


if __name__ == "__main__":
    try:
        payload = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())["client_payload"]
        print(synchronize(GitHub(os.environ["DOCS_TOKEN"]), GitHub(os.environ["CODE_TOKEN"]), payload))
    except Blocked as exc:
        sys.exit(str(exc))
    except (KeyError, TypeError, ValueError, OSError):
        sys.exit("Docs sync could not verify the GitHub response or an input file.")
