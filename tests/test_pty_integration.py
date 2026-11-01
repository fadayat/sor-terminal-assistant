import os
from pathlib import Path
import tempfile
import unittest

try:
    import pexpect
except ImportError:  # pragma: no cover - optional test dependency
    pexpect = None


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf(pexpect is None, "pexpect is not installed")
class PtyIntegrationTests(unittest.TestCase):
    def test_commands_are_captured_once_and_session_files_are_removed(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            home = base / "home"
            runtime = base / "runtime"
            home.mkdir()
            runtime.mkdir(mode=0o700)
            (home / ".bashrc").write_text(
                "PS1='SOR_TEST_PROMPT> '\n"
                f"source {ROOT / 'bash/sor-session.bash'}\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.update(
                {
                    "HOME": str(home),
                    "XDG_RUNTIME_DIR": str(runtime),
                    "TERM": "xterm-256color",
                    "SHELL": "/bin/bash",
                }
            )
            child = pexpect.spawn(
                str(ROOT / "bin/sor-session-recorder"),
                env=environment,
                encoding="utf-8",
                timeout=10,
            )
            try:
                child.expect_exact("SOR_TEST_PROMPT> ")
                child.sendline("echo SOR_PTY_MARKER")
                child.expect_exact("SOR_PTY_MARKER")
                child.expect_exact("SOR_TEST_PROMPT> ")
                child.sendline("false")
                child.expect_exact("SOR_TEST_PROMPT> ")
                child.sendline('wc -l < "$SOR_SESSION_EVENTS"')
                child.expect_exact("\r2\r\n")
                child.expect_exact("SOR_TEST_PROMPT> ")
                child.sendline("exit")
                child.expect(pexpect.EOF)
            finally:
                if child.isalive():
                    child.sendline("exit")
                    child.close(force=True)

            session_directory = runtime / "sor-sessions"
            self.assertEqual(list(session_directory.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
