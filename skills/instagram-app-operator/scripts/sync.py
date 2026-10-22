#!/usr/bin/env python3
"""Save only reviewed skill files. Never ingest chats or phone records."""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys

PREFIX = "skills/instagram-app-operator/"
FILES = ("SKILL.md", "agents/openai.yaml", "references/mirror-recovery.md",
         "references/field-notes.md", "references/persistence.md",
         "scripts/sync.py", "scripts/test_sync.py")
ALLOWED = {PREFIX + name for name in FILES}


class SyncError(Exception):
    pass


def inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def synchronize(config, check=False):
    repo = Path(config["repo"]).expanduser().resolve()
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    base = ["git"]
    if config.get("http_proxy"):
        base += ["-c", "http.proxy=" + config["http_proxy"]]

    def git(*args):
        result = subprocess.run(base + list(args), cwd=str(repo), env=env,
                                capture_output=True, text=True, timeout=35)
        if result.returncode:
            # Git errors can contain credential-bearing URLs; never copy stderr.
            raise SyncError("git " + args[0] + " failed; changes kept locally")
        return result.stdout.strip()

    if Path(git("rev-parse", "--show-toplevel")).resolve() != repo:
        raise SyncError("Configured path must be the repository root")
    if git("symbolic-ref", "--short", "HEAD") != config["branch"]:
        raise SyncError("Unexpected branch; no automatic checkout")
    if git("remote", "get-url", "origin") != config["expected_remote"]:
        raise SyncError("Unexpected remote")
    if git("remote", "get-url", "--push", "origin") != config["expected_remote"]:
        raise SyncError("Unexpected push destination")
    git_dir = Path(git("rev-parse", "--absolute-git-dir"))
    if any((git_dir / name).exists() for name in
           ("MERGE_HEAD", "CHERRY_PICK_HEAD", "rebase-merge", "rebase-apply")):
        raise SyncError("Git operation in progress")
    if git("diff", "--name-only", "--diff-filter=U"):
        raise SyncError("Unresolved conflicts")
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    if staged - ALLOWED:
        raise SyncError("Other files are staged; preserve the user's index")
    extra = set(git("ls-files", "--others", "--exclude-standard", "--", PREFIX).splitlines())
    if extra - ALLOWED:
        raise SyncError("Unreviewed files in the skill directory")
    for name in FILES:
        path = repo / PREFIX / name
        if path.is_symlink() or not inside(path.resolve(), repo):
            raise SyncError("Symlink or path outside repository")
        if not path.is_file() or path.stat().st_size > 131072:
            raise SyncError("Missing or oversized skill file")
    changed = set(git("diff", "HEAD", "--name-only", "--", PREFIX).splitlines()) | extra
    if changed - ALLOWED:
        raise SyncError("Changes outside the reviewed file allowlist")
    remote_ref = "refs/remotes/origin/" + config["branch"]
    pending = git("rev-list", remote_ref + "..HEAD").splitlines()
    if check:
        return {"state": "checked", "changed_files": sorted(changed),
                "pending_commits": len(pending)}
    if not changed and not pending:
        return {"state": "unchanged"}
    git("fetch", "--quiet", "origin", config["branch"])
    git("merge-base", "--is-ancestor", remote_ref, "HEAD")
    for revision in git("rev-list", remote_ref + "..HEAD").splitlines():
        touched = set(git("diff-tree", "--root", "--no-commit-id", "--name-only",
                          "-r", revision).splitlines())
        parents = git("rev-list", "--parents", "-n", "1", revision).split()
        if touched - ALLOWED or len(parents) > 2:
            raise SyncError("Unrelated or merge commits are pending; review required")
    if changed:
        git("add", "--", *sorted(ALLOWED))
        git("diff", "--cached", "--check")
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        git("commit", "-m", "Update Instagram operator workflow (" + stamp + ")")
    head = git("rev-parse", "HEAD")
    git("push", "origin", "HEAD:refs/heads/" + config["branch"])
    remote = git("ls-remote", "origin", "refs/heads/" + config["branch"]).split()
    if not remote or remote[0] != head:
        raise SyncError("Push was not verified at the remote")
    return {"state": "pushed", "commit": head}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--hook", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    config_path = Path(args.config).expanduser()
    try:
        event = json.load(sys.stdin) if args.hook else {}
        config = json.loads(config_path.read_text())
        if args.hook:
            cwd = Path(event.get("cwd", "/")).resolve()
            roots = [Path(root).expanduser().resolve() for root in config["scope_roots"]]
            if event.get("hook_event_name") != "Stop" or not any(inside(cwd, root) for root in roots):
                print("{}")
                return 0
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with (config_path.parent / "sync.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                print("{}" if args.hook else '{"state":"busy"}')
                return 0
            result = synchronize(config, args.check)
        result["observed_at"] = datetime.now(timezone.utc).isoformat()
        result["source"] = "Stop" if args.hook else "manual"
        status = config_path.parent / "sync-status.json"
        temporary = status.with_suffix(".tmp")
        temporary.write_text(json.dumps(result, indent=2) + "\n")
        temporary.replace(status)
        print("{}" if args.hook else json.dumps(result))
        return 0
    except (SyncError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        message = str(error) if isinstance(error, SyncError) else type(error).__name__
        result = {"state": "pending", "reason": message,
                  "source": "Stop" if args.hook else "manual"}
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            (config_path.parent / "sync-status.json").write_text(json.dumps(result) + "\n")
        except OSError:
            pass
        print(json.dumps({"systemMessage": "Instagram workflow sync pending: " + message})
              if args.hook else json.dumps(result))
        return 0 if args.hook else 1


if __name__ == "__main__":
    sys.exit(main())
