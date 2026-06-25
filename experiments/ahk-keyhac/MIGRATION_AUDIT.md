# AHK Migration Audit

Scope: migrate only personal `keyhac-win/custom_config` and `keyhac-win/extensions` behavior that is independent of bundled Keyhac sample functionality.

## Completed / Base Layer

| Feature | Current Keyhac source | AHK status | Notes |
| --- | --- | --- | --- |
| `U0-U4` virtual modifiers | `custom_config/main.py` | Done | Kanata `F19-F23` -> AHK `U0-U4`. |
| `U0-C` copy path/copy | `custom_config/main.py` | Done | In supported terminals copy cwd; otherwise `Alt+D`, `Ctrl+C`. |
| `U0` mouse layer | `extensions/input/mouse_ext.py` | Done with adjusted chords | AHK uses `U0-*`, not Keyhac `U0-A-*`, to preserve `U0+Alt => LWin`. |
| `C-U0-Left/Right/Up/Down` window move | `custom_config/main.py` | Done | User-selected chord for active-window 10px movement. |
| `U0-lalt` native Win tap | Kanata/Keyhac combination semantics | Done | AHK passthrough patch preserves `U0-lalt-other-key`. |

## P1: Low Risk

| Feature | Chord | Source | Migration recommendation |
| --- | --- | --- | --- |
| Copy selection then `Alt+L` | `U0-A` | `extensions/clipboard/clipboard_ext.py`, `extensions/clipboard/clipboard_commands.py` | Direct AHK migration. Probe selection via clipboard, then pass through `Alt+L`. |
| App launcher, simple version | `U0-Space` | `extensions/apps/app_launcher.py` | Start with a simple menu for Notepad/Paint, then upgrade to a reusable picker. |
| Editor basics | `C-D`, `C-H` in `Edit`; Notepad `C-P/N/F/B/A/E/Y`, `C-X C-S` | `extensions/ui/editor_ext.py` | Good fit for AHK `#HotIf` window-scoped bindings. |

## P2: Requires Picker/List Infrastructure

| Feature | Chord | Source | Migration recommendation |
| --- | --- | --- | --- |
| Window switcher | `U0-W` | `extensions/window/window_switcher.py` | Implement reusable AHK picker first: enumerate windows, filter, Enter to activate. |
| Clipboard history search | `U1-Semicolon` | `custom_config/main.py`, `extensions/clipboard/clipboard_ext.py` | Keyhac built-in history cannot be reused directly. Choose AHK-owned history or CopyQ integration. |
| List window controls | `C-J/K/H/L`, `Esc`, `C-S-D` | `extensions/window/list_window_ext.py` | Fold into the AHK picker instead of porting Keyhac list-window internals. |

## P3: PowerKey / Multi-Key Sequences

| Feature | Chord/sequence | Source | Migration recommendation |
| --- | --- | --- | --- |
| Git prompt snippets | `g c-p`, `g p-p`, `g l-c` | `extensions/ui/coding_ext.py`, `extensions/ui/snippet_sequences.py` | Build AHK sequence engine first, then migrate snippets. |
| Terminal matrix | `s p-7`, `s p-5`, `r p-7`, `r p-5`, `g p-7`, `g p-5` | `extensions/ui/terminal_matrix_ext.py` | Depends on sequence engine and external terminal launch details. |
| URL launcher framework | registered sequences | `extensions/apps/url_launcher.py` | No concrete registration found in current entry point; keep as reusable later design. |

## P4: App-Specific

| Feature | Chord/sequence | Source | Migration recommendation |
| --- | --- | --- | --- |
| TeXstudio bracket helpers | `U2-C/D/X/S/V/F` in `texstudio.exe` | `extensions/tex/texstudio_ext.py`, `extensions/tex/texstudio_commands.py` | Can migrate independently with `#HotIf WinActive("ahk_exe texstudio.exe")`; medium risk due to clipboard and delay handling. |
| TeXstudio PowerKey colors/snippets | `f n`, `n b`, `m r`, `p l/g`, `g r`, `b l`, plus git snippets | `extensions/tex/texstudio_ext.py` | Depends on sequence engine and smart clipboard insert. |

## Low Priority / Possibly No Migration

| Module | Reason |
| --- | --- |
| `extensions/apps/komorebi_ext.py`, `extensions/apps/komorebi_runtime.py` | `build_komorebi_bindings()` currently returns `{}`; pure komorebi hotkeys have moved to Kanata. |
| `extensions/system/shared_state.py` | Mostly serves Keyhac/Kanata/YASB state publishing. Defer unless AHK takes over status publishing. |
| `extensions/input/key_inject.py` | Python SendInput helper; AHK has native `Send`/`SendEvent`. |
| `extensions/input/powerkey_ext.py` | Do not port line-for-line; implement an AHK sequence engine. |
