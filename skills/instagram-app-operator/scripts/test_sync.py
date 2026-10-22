"""Exercise real Git commits/pushes against temporary local remotes."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("skill_sync", Path(__file__).with_name("sync.py"))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, capture_output=True)
        subprocess.run(["git", "init", str(self.repo)], check=True, capture_output=True)
        self.git("checkout", "-b", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        for relative in sync.ALLOWED:
            path = self.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("initial\n")
        self.git("add", ".")
        self.git("commit", "-m", "Fixture")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")
        self.config = {"repo": str(self.repo), "expected_remote": str(self.remote),
                       "branch": "main", "scope_roots": [str(self.repo)]}

    def git(self, *args):
        return subprocess.run(["git"] + list(args), cwd=self.repo, check=True,
                              capture_output=True, text=True).stdout.strip()

    def change(self):
        (self.repo / sync.PREFIX / "references/field-notes.md").write_text("verified lesson\n")

    def test_push_and_no_empty_commit(self):
        self.change()
        (self.repo / "unrelated.txt").write_text("leave alone")
        result = sync.synchronize(self.config)
        self.assertEqual(result["state"], "pushed")
        head = self.git("rev-parse", "HEAD")
        self.assertEqual(head, self.git("ls-remote", "origin", "refs/heads/main").split()[0])
        self.assertEqual(sync.synchronize(self.config)["state"], "unchanged")
        self.assertEqual(head, self.git("rev-parse", "HEAD"))
        self.assertIn("unrelated.txt", self.git("status", "--porcelain"))

    def test_preserves_unrelated_index(self):
        self.change()
        (self.repo / "unrelated.txt").write_text("staged by user")
        self.git("add", "unrelated.txt")
        with self.assertRaisesRegex(sync.SyncError, "Other files are staged"):
            sync.synchronize(self.config)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "unrelated.txt")

    def test_rejects_private_extra_and_symlink(self):
        private = self.repo / sync.PREFIX / "private.json"
        private.write_text('{}')
        with self.assertRaisesRegex(sync.SyncError, "Unreviewed files"):
            sync.synchronize(self.config)
        private.unlink()
        path = self.repo / sync.PREFIX / "references/field-notes.md"
        path.unlink()
        path.symlink_to(self.root / "outside")
        with self.assertRaisesRegex(sync.SyncError, "Symlink"):
            sync.synchronize(self.config)

    def test_rejects_unrelated_unpushed_commit(self):
        (self.repo / "unrelated.txt").write_text("do not push")
        self.git("add", "unrelated.txt")
        self.git("commit", "-m", "Unrelated")
        with self.assertRaisesRegex(sync.SyncError, "Unrelated"):
            sync.synchronize(self.config)

    def test_remote_advance_keeps_work_local(self):
        clone = self.root / "other"
        subprocess.run(["git", "clone", "-b", "main", str(self.remote), str(clone)],
                       check=True, capture_output=True)
        subprocess.run(["git", "-C", str(clone), "config", "user.name", "Fixture"], check=True)
        subprocess.run(["git", "-C", str(clone), "config", "user.email", "fixture@example.invalid"], check=True)
        (clone / "advance").write_text("remote update")
        for args in [("add", "."), ("commit", "-m", "Advance"), ("push",)]:
            subprocess.run(["git", "-C", str(clone)] + list(args), check=True, capture_output=True)
        self.change()
        with self.assertRaises(sync.SyncError):
            sync.synchronize(self.config)
        self.assertEqual((self.repo / sync.PREFIX / "references/field-notes.md").read_text(), "verified lesson\n")

    def test_hook_ignores_other_workspaces(self):
        config = self.root / "state" / "local.json"
        config.parent.mkdir()
        config.write_text(json.dumps(self.config))
        result = subprocess.run(["python3", str(Path(sync.__file__)), "--config", str(config), "--hook"],
                                input=json.dumps({"hook_event_name": "Stop", "cwd": str(self.root / "other")}),
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertFalse((config.parent / "sync-status.json").exists())

    def test_hook_pushes_only_files_and_records_source(self):
        self.change()
        config = self.root / "state" / "local.json"
        config.parent.mkdir()
        config.write_text(json.dumps(self.config))
        result = subprocess.run(["python3", str(Path(sync.__file__)), "--config", str(config), "--hook"],
                                input=json.dumps({"hook_event_name": "Stop", "cwd": str(self.repo),
                                                  "last_assistant_message": "PRIVATE_FIXTURE_NEVER_EXPORT"}),
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), {})
        status = json.loads((config.parent / "sync-status.json").read_text())
        self.assertEqual(status["state"], "pushed")
        self.assertEqual(status["source"], "Stop")
        self.assertNotIn("PRIVATE_FIXTURE_NEVER_EXPORT", self.git("show", "HEAD"))

    def test_wrong_remote_and_missing_file_are_rejected(self):
        self.change()
        config = dict(self.config, expected_remote="unexpected")
        with self.assertRaisesRegex(sync.SyncError, "Unexpected remote"):
            sync.synchronize(config)
        (self.repo / sync.PREFIX / "SKILL.md").unlink()
        with self.assertRaisesRegex(sync.SyncError, "Missing"):
            sync.synchronize(self.config)


if __name__ == "__main__":
    unittest.main()
