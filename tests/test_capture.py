import importlib.util
from importlib.machinery import SourceFileLoader
import json
import os
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    loader = SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


event = load_module("sor_session_event", ROOT / "bin/sor-session-event")
recorder = load_module("sor_session_recorder", ROOT / "bin/sor-session-recorder")


class SessionEventTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name)
        self.directory = base / "sor-sessions"
        self.directory.mkdir(mode=0o700)
        self.log_path = self.directory / "terminal-1.log"
        self.events_path = self.directory / "terminal-1.events.jsonl"
        self.start_path = self.directory / "terminal-1.start"
        self.pause_path = self.directory / "terminal-1.paused"
        for path in (self.log_path, self.events_path, self.start_path):
            descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(descriptor)
        self.original_environment = os.environ.copy()
        os.environ.update(
            {
                "SOR_SESSION_LOG": str(self.log_path),
                "SOR_SESSION_EVENTS": str(self.events_path),
                "SOR_SESSION_START_FILE": str(self.start_path),
                "SOR_SESSION_PAUSE_FILE": str(self.pause_path),
            }
        )
        self.addCleanup(self._restore_environment)

    def _restore_environment(self):
        os.environ.clear()
        os.environ.update(self.original_environment)

    def test_start_and_finish_write_structured_record(self):
        event.begin_command()
        event.finish_command(7, str(self.directory), "false")

        record = json.loads(self.events_path.read_text().strip())
        self.assertEqual(record["type"], "command")
        self.assertEqual(record["command"], "false")
        self.assertEqual(record["exit_code"], 7)
        self.assertEqual(record["cwd"], str(self.directory))
        self.assertIsInstance(record["started_at"], float)
        self.assertIsInstance(record["finished_at"], float)
        self.assertIsInstance(record["duration_ms"], int)
        self.assertEqual(self.events_path.stat().st_mode & 0o777, 0o600)

    def test_pause_suppresses_event_write(self):
        self.pause_path.write_text("paused")
        event.begin_command()
        event.finish_command(0, str(self.directory), "echo hidden")
        self.assertEqual(self.events_path.read_text(), "")

    def test_finish_without_start_does_not_capture_old_history(self):
        event.finish_command(0, str(self.directory), "old history command")
        self.assertEqual(self.events_path.read_text(), "")

    def test_rejects_event_path_outside_session_directory(self):
        outside = Path(self.temporary.name) / "outside.jsonl"
        outside.touch(mode=0o600)
        os.environ["SOR_SESSION_EVENTS"] = str(outside)
        with self.assertRaises(event.SessionEventError):
            event.validated_session_file("SOR_SESSION_EVENTS")

    def test_accepts_in_directory_symlink_target(self):
        link = self.directory / "linked.events.jsonl"
        link.symlink_to(self.events_path)
        os.environ["SOR_SESSION_EVENTS"] = str(link)
        self.assertEqual(event.validated_session_file("SOR_SESSION_EVENTS"), self.events_path)

    def test_invalid_pause_path_fails_closed(self):
        outside = Path(self.temporary.name) / "outside.paused"
        outside.touch(mode=0o600)
        os.environ["SOR_SESSION_PAUSE_FILE"] = str(outside)
        self.assertTrue(event.is_paused())


class RecorderPathTests(unittest.TestCase):
    def test_cleanup_removes_exact_session_files(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / name for name in ("log", "events", "start", "paused")]
            for path in paths:
                path.touch()
            recorder.remove_session_files(paths)
            self.assertTrue(all(not path.exists() for path in paths))

    def test_private_file_creation_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.log"
            descriptor = recorder.create_private_file(path)
            os.close(descriptor)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
