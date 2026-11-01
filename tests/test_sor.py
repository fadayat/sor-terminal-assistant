import importlib.util
from importlib.machinery import SourceFileLoader
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "bin" / "sor"
SPEC = importlib.util.spec_from_loader("sor_cli", SourceFileLoader("sor_cli", str(MODULE_PATH)))
sor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sor)


class SorCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name) / "sor-sessions"
        self.directory.mkdir(mode=0o700)
        self.log_path = self.directory / "terminal.log"
        self.events_path = self.directory / "terminal.jsonl"
        self.log_path.write_text("hello from terminal\n", encoding="utf-8")
        self.events_path.write_text("", encoding="utf-8")
        self.env = mock.patch.dict(
            os.environ,
            {
                "SOR_SESSION_LOG": str(self.log_path),
                "SOR_SESSION_EVENTS": str(self.events_path),
            },
            clear=False,
        )
        self.env.start()
        self.directory_patch = mock.patch.object(sor, "session_directory", return_value=self.directory)
        self.directory_patch.start()

    def tearDown(self):
        self.directory_patch.stop()
        self.env.stop()
        self.temporary.cleanup()

    def write_events(self, events):
        self.events_path.write_text(
            "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
        )

    @staticmethod
    def event(command, code=0):
        return {
            "type": "command",
            "command": command,
            "exit_code": code,
            "cwd": "/tmp/work",
            "started_at": 1.0,
            "finished_at": 2.0,
            "duration_ms": 1000,
        }

    def test_cli_parses_modes_and_last_count(self):
        args = sor.parse_cli(["--last", "2", "fix", "why", "failed"])
        self.assertEqual(args.target, "fix")
        self.assertEqual(args.question, ["why", "failed"])
        self.assertEqual(args.last, 2)
        with self.assertRaises(SystemExit):
            sor.parse_cli(["--last", "0", "hello"])
        self.assertTrue(sor.parse_cli(["--status"]).status)

    def test_modes_keep_safe_prompts_and_reasoning_defaults(self):
        self.assertIn("Əmri heç vaxt icra etmə", sor.mode_instruction("fix"))
        self.assertIn("Yalnız işlədiləcək shell əmrini", sor.mode_instruction("cmd"))
        self.assertEqual(sor.reasoning_effort("ask"), "low")
        self.assertEqual(sor.reasoning_effort("fix"), "low")
        self.assertEqual(sor.reasoning_effort("cmd"), "low")
        self.assertEqual(sor.reasoning_effort("deep"), "high")

    def test_context_uses_last_n_structured_records(self):
        self.write_events([self.event("one"), self.event("two"), self.event("three")])
        context = sor.terminal_session_context(last=2)
        self.assertNotIn("Komanda: one", context)
        self.assertIn("Komanda: two", context)
        self.assertIn("Komanda: three", context)
        self.assertIn("hello from terminal", context)

    def test_context_rejects_outside_session_file(self):
        outside = Path(self.temporary.name) / "outside.log"
        outside.write_text("should not be read", encoding="utf-8")
        with mock.patch.dict(os.environ, {"SOR_SESSION_LOG": str(outside)}):
            self.assertEqual(sor.terminal_session_context(), "")

    def test_secrets_are_redacted(self):
        github_token = "ghp_" + ("x" * 36)
        openai_token = "sk-proj-" + ("y" * 32)
        private_key = "-----BEGIN " + "PRIVATE KEY-----\nsecret body\n-----END PRIVATE KEY-----"
        text = (
            "Authorization: Bearer abc.def token=abc "
            f"GITHUB_TOKEN={github_token} "
            f"{openai_token} "
            f"{private_key}"
        )
        redacted = sor.redact_secrets(text)
        self.assertNotIn("abc.def", redacted)
        self.assertNotIn(github_token, redacted)
        self.assertNotIn(openai_token, redacted)
        self.assertNotIn("secret body", redacted)
        self.assertGreaterEqual(redacted.count("[REDACTED]"), 5)

    def test_no_arguments_auto_uses_last_command_in_tty(self):
        self.write_events([self.event("false", code=1)])

        class TtyInput:
            def isatty(self):
                return True

            def read(self):
                return ""

        with (
            mock.patch.object(sor.sys, "argv", ["sor"]),
            mock.patch.object(sor.sys, "stdin", TtyInput()),
            mock.patch.object(sor, "ask") as ask,
        ):
            self.assertEqual(sor.main(), 0)
        ask.assert_called_once()
        self.assertIn("Son terminal komandam", ask.call_args.args[0])
        self.assertEqual(ask.call_args.kwargs["mode"], "ask")

    def test_pause_resume_and_clear_controls(self):
        self.assertEqual(sor.manage_session("pause"), 0)
        self.assertTrue(sor.is_session_paused(self.log_path))
        self.assertEqual(sor.terminal_session_context(), "")
        self.assertEqual(sor.manage_session("resume"), 0)
        self.assertFalse(sor.is_session_paused(self.log_path))
        self.write_events([self.event("printf test")])
        self.assertEqual(sor.manage_session("clear"), 0)
        self.assertEqual(self.log_path.read_bytes(), b"")
        self.assertEqual(self.events_path.read_bytes(), b"")
        self.assertEqual((self.directory / "terminal.paused").exists(), False)


if __name__ == "__main__":
    unittest.main()
