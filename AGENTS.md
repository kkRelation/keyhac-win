# Repository Guidelines

## Project Structure & Module Organization
This repository is a portable Keyhac setup for Windows. The main entry point is `keyhac.exe`, with a root `config.py` shim that delegates to `custom_config/main.py`. Put reusable automation logic in domain folders under `extensions/`. Built-in runtime files live under `modules/` and should be treated as vendored internals. Reference docs are in `doc/en/`, `doc/ja/`, and `docs/`; themes are in `theme/`, and Migemo dictionaries are in `dict/`.

## Build, Test, and Development Commands
There is no local build pipeline in this distribution; development is configuration-driven.

- `.\keyhac.exe`: launch Keyhac with this repo as the working config.
- Reload from the tray menu after editing `config.py`, `custom_config/`, or `extensions/`.
- `python -m py_compile config.py custom_config\main.py extensions\**\*.py`: quick syntax check for edited scripts when a matching Python is available.

Use `doc/en/index.html` for API details and `docs/architecture/GEMINI.md` for repository-specific notes.

## Coding Style & Naming Conventions
Use Python with 4-space indentation and keep module-level setup simple. Follow the existing pattern of `init_<feature>(keymap, ...)` for extension entry points and `command_<Action>` for callable commands. Prefer `snake_case` for functions and variables, and keep key binding names explicit, for example `keymap_global["U0-Space"]`. Match the surrounding file style when editing older code.

## Testing Guidelines
This repo does not include an automated test suite. Validate changes by:

- Running `python -m py_compile ...` for syntax.
- Launching `.\keyhac.exe`.
- Reloading the config from the tray.
- Exercising the affected hotkeys or list windows manually.

For behavior changes, verify both the target app flow and that global bindings still work.

## Commit & Pull Request Guidelines
Recent history uses short, imperative subjects, usually with a Conventional Commit prefix such as `feat:` (`feat: change TeXstudio trigger keys from Caps+K/L to Caps+S/D`). Keep commits focused on one behavior change. Pull requests should include a concise summary, the affected bindings or modules, manual verification steps, and screenshots only when UI elements such as list windows or themes changed.

## Configuration & Safety Notes
Do not edit `modules/` unless you intentionally need to patch vendored runtime code. Avoid committing machine-specific secrets, paths, or personal clipboard snippets in `custom_config/main.py` and clipboard extensions.
