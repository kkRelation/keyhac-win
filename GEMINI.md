# Keyhac - Python Powered Key Customization Tool

Keyhac is a highly flexible keyboard customization application for Windows (10/11 64-bit) that allows users to describe their keyboard behavior using Python scripts. It provides a resident tasktray icon, a console for log output, and a rich API for window and input manipulation.

## Project Overview

- **Purpose:** Advanced keyboard and mouse automation, key remapping, and window management.
- **Core Technology:** Python 3.13 (embedded), PyAuto (window/input manipulation), and CKit (UI/Utility library).
- **Key Features:**
  - **Key Remapping:** Simple replacements or complex multi-stroke (Emacs-style) keybindings.
  - **Modifiers:** Custom modifier keys (User0-User3) and "One-shot" modifiers (actions on tap).
  - **Context-Aware:** Different keymaps for specific applications (based on executable name or window class).
  - **Clipboard History:** Built-in history manager with support for fixed phrases and custom transformations.
  - **Automation:** Window movement, application launching, virtual mouse control, and keyboard macros.
  - **Extensibility:** Users can write arbitrary Python code to handle key events.

## Directory Structure

- `keyhac.exe`: The main application executable.
- `_config.py`: The default configuration template. Users typically edit `config.py` (created in AppData or the local directory upon first run).
- `modules/keyhac/`: Core application logic (distributed as `.pyc` files).
- `modules/Lib/`: Embedded Python standard library and third-party dependencies (`pyauto`, `ckit`, `PIL`).
- `doc/`: Comprehensive documentation in English (`doc/en/`) and Japanese (`doc/ja/`).
- `theme/`: Visual themes for the console and list windows.
- `extension/`: A directory for user-defined extension scripts.
- `dict/`: Directory for Migemo dictionary files (for Japanese incremental search).

## Development and Configuration

### Configuration Workflow
1. **Launch Keyhac:** Run `keyhac.exe`.
2. **Edit Config:** Right-click the tasktray icon and select "Edit config file". This opens `config.py`.
3. **Customize:** Define your keymaps inside the `configure(keymap)` function.
4. **Reload:** Right-click the tasktray icon and select "Reload config file" to apply changes.
5. **Debug:** Use the console window (left-click icon) to view `print()` output or Python errors.

### Key API Concepts
- `keymap.replaceKey(old, new)`: Globally replace one key with another.
- `keymap.defineModifier(key, name)`: Define a new modifier key.
- `keymap.defineWindowKeymap(...)`: Create a keymap scoped to specific windows or global.
- `keymap.InputTextCommand(text)`: Create a command that types specific text.
- `keymap.ShellExecuteCommand(...)`: Create a command that runs a program or opens a URL.

### PowerKey Sequence Management
- Letter-sequence bindings such as `f-n`, `g-c-p`, and `g-p-p` are managed by `extension/powerkey_ext.py`.
- For any single window scope such as `exe_name="texstudio.exe"`, always reuse one shared `PowerKeyManager` via `PowerKeyManager.for_scope(...)`.
- Do not instantiate multiple `PowerKeyManager` objects for the same scope. Multiple managers on the same `window_keymap` can overwrite each other's letter-key handlers and break sequence matching.
- Use `PowerKeyManager.add(...)` as the default template entry point:
  - Single-step suffixes like `{"n": action}` map to two-key sequences such as `f-n`.
  - Multi-step suffixes like `{"c-p": action}` map to three-key or n-key sequences such as `g-c-p` or `g-p-p`.
  - **Tapping Support:** Sequences can be triggered by tapping the suffix keys while holding the prefix, or by using OS auto-repeat. Intermediate key releases do not cancel the sequence.
- Keep default trigger behavior implicit unless a scope needs a special override:
  - Single-step suffixes default to `trigger_on="up"`.
  - Multi-step suffixes default to `trigger_on="down"`.

## Documentation References
For detailed API documentation, refer to:
- **English:** `doc/en/index.html`
- **Japanese:** `doc/ja/index.html`

## Building and Running
This project is typically distributed as a portable binary.
- **To Run:** Execute `keyhac.exe`.
- **To Build:** The author uses Python 3.13 + Visual Studio 2022. Building from source would require the original `.py` files and the C++ source for the host executable (not present in this distribution).
- **Dependencies:** Managed via the internal `modules/Lib` directory. Do not modify these manually.
