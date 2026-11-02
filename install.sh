#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BIN_DIR=${SOR_BIN_DIR:-"${HOME}/.local/bin"}
BASHRC_DIR=${SOR_BASHRC_DIR:-"${HOME}/.bashrc.d"}

if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' 'Sor requires Python 3.11 or newer.' >&2
    exit 1
fi
if ! python3 -c 'import sys, tomllib; assert sys.version_info >= (3, 11)' >/dev/null 2>&1; then
    printf '%s\n' 'Sor requires Python 3.11 or newer (tomllib is required).' >&2
    exit 1
fi
if ! python3 -c 'import websockets.sync.client' >/dev/null 2>&1; then
    printf '%s\n' 'Missing Python package: websockets. Install it with: python3 -m pip install --user websockets' >&2
    exit 1
fi

mkdir -p "$BIN_DIR" "$BASHRC_DIR"
install -m 0755 "$ROOT/bin/sor" "$BIN_DIR/sor"
install -m 0755 "$ROOT/bin/sor-session-recorder" "$BIN_DIR/sor-session-recorder"
install -m 0755 "$ROOT/bin/sor-session-event" "$BIN_DIR/sor-session-event"
install -m 0644 "$ROOT/bash/sor-session.bash" "$BASHRC_DIR/sor-session.bash"

if ! command -v codex >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/codex" ]; then
    printf '%s\n' 'Installed Sor, but Codex CLI was not found.' \
        'Install Codex CLI and sign in, then configure provider.codex_home/provider.codex_bin if needed.' >&2
else
    printf '%s\n' 'Codex CLI found. Sor will use its local app-server after Codex is signed in.'
fi

printf 'Installed Sor commands into %s\n' "$BIN_DIR"
printf 'Installed Bash hook into %s/sor-session.bash\n' "$BASHRC_DIR"
printf '%s\n' 'The installer did not modify ~/.bashrc.'
printf '%s\n' 'If your ~/.bashrc does not load ~/.bashrc.d/*.bash, add this line manually:'
printf '  for f in "%s"/*.bash; do [ -r "$f" ] && . "$f"; done\n' "$BASHRC_DIR"
printf '%s\n' 'Open a new terminal, then run: sor --status'
