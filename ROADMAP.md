# Sor roadmap

This roadmap separates capabilities already present in the repository from ideas that still need implementation. Sor is an early-stage project; priorities may change based on real use and community feedback.

## Shipped

- Terminal question command with `ask`, `fix`, `cmd`, `deep`, and `full` modes.
- Local Codex app-server connection using the user's existing Codex sign-in.
- Streaming answers and a waiting indicator.
- Interactive VTE Bash PTY capture with structured command metadata and output markers.
- Local relevance matching over the current terminal session, plus raw-tail fallback.
- Session controls: `--status`, `pause`, `resume`, and `clear`.
- Best-effort secret redaction before terminal context is sent.
- `./install.sh` installer and configuration through `config.toml` or environment variables.

## Planned: provider layer

Sor currently talks to a locally authenticated Codex app-server. The next provider architecture should preserve one terminal workflow while allowing users to choose how requests are served.

- Separate the terminal/context pipeline from provider-specific transport and authentication.
- Add optional OpenAI API support with user-supplied credentials loaded from environment variables or a secure local source. Secrets must never be committed to the repository or copied into terminal context.
- Add configurable OpenAI-compatible endpoints for supported local and self-hosted models.
- Evaluate first-class adapters for Ollama, LM Studio, and llama.cpp instead of claiming compatibility before it is tested.
- Support multiple named profiles for different providers, models, endpoints, and reasoning settings.
- Add provider discovery, configuration validation, health checks, and actionable connection errors.
- Make streaming, cancellation, timeouts, and context limits consistent across providers where their capabilities allow it.
- Document clearly when a provider requires an API key, a local service, an existing product sign-in, or usage-based billing.

## Planned: terminal experience

- Improve command/output matching for asynchronous jobs, multiline commands, and unusual shell history settings.
- Add a doctor command and clearer configuration validation.
- Add persistent conversation support within a terminal session, with an explicit reset command.
- Add an optional keybinding that places a suggested command on the prompt for review.
- Improve context controls so users can inspect and adjust what a question will send.
- Evaluate Zsh and Fish support after the Bash capture path is more mature.

## Later ideas

- Optional project and Git context.
- File, image, or clipboard input.
- More context-selection and privacy controls.

These are ideas, not current features or commitments. Sor will not claim support for a provider, shell, or workflow until it has been implemented and documented.
