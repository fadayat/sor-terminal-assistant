# Contributing

Sor is early-stage software. Bug reports, documentation fixes, and focused
improvements are welcome. For a large behavioral change, open an issue first so
the design and scope can be discussed before implementation.

## Local setup

Sor requires Linux, Bash, Python 3.11 or newer, the Python `websockets` package,
and a locally authenticated Codex CLI installation.

```bash
git clone https://github.com/fadayat/sor-terminal-assistant.git
cd sor-terminal-assistant
./install.sh
```

The focused test suite can be run with:

```bash
python3 -m unittest discover -s tests -v
```

## Pull requests

- Keep changes focused and preserve the rule that suggested commands require
  user review.
- Do not add credentials, terminal logs, personal paths, or account data.
- Update the README when user-visible behavior changes.
- Describe what changed, why it changed, and any known limitation.
- Add or update focused tests when behavior changes.

When reporting a bug, sanitize terminal output before attaching it. Terminal
logs can contain tokens, paths, hostnames, and other private information.
