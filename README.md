# Keyhac Custom Actions

This repository keeps the Keyhac runtime at the repo root and user-defined automation in `custom_config/`, `extensions/`, `tools/`, and `generated/`.

Shortcut ownership is documented in [docs/hotkeys/HOTKEY_OWNERSHIP.md](docs/hotkeys/HOTKEY_OWNERSHIP.md).

## Maintenance Rule

When adding a new custom action:

1. Register the behavior in code.
2. Add or update the corresponding row in the table below in the same change.

When adding power-key letter sequences such as `f-n` or `g-c-p`:

1. Reuse the existing `PowerKeyManager` for the same scope via `PowerKeyManager.for_scope(...)`.
2. Do not create multiple `PowerKeyManager` instances for the same `exe_name` or other window scope.

## Custom Action Table

| Shortcut | Scope | Behavior | Source |
| --- | --- | --- | --- |
| `U1-A` | Global | Send the native `CapsLock` key | `kanata_config/win_to_f19.kbd` |
| `C-A-S-7` / `C-A-S-8` / `C-A-S-9` / `C-A-S-0` / `C-A-S--` | Global | Toggle `RAlt` / `RCtrl` / `RShift` / `Win` / `Caps` User-mode state | `custom_config/main.py` |
| `U0+Alt` | Global | Send the native `LWin` key | `kanata_config/win_to_f19.kbd` |
| `Ctrl+U1` / `U1+Ctrl` | Global | Toggle komorebi modal mode on/off | `kanata_config/win_to_f19.kbd` |
| `C-S-A-U` | Global | Toggle all five User-mode states on/off together | `custom_config/main.py` |
| `U1+;` | Global | Open clipboard history list and start incremental search | `custom_config/main.py` |
| `U0-0` | Global | Toggle macro recording | `custom_config/main.py` |
| `U0-3` | Global | Play the recorded macro | `custom_config/main.py` |
| `U0-Left` / `U0-Right` / `U0-Up` / `U0-Down` | Global | Move the current window by 10px | `custom_config/main.py` |
| `U0-Space` | Global | Open the application launcher list and start incremental search | `extensions/apps/app_launcher.py` |
| `U0-A-Left` / `U0-A-Right` / `U0-A-Up` / `U0-A-Down` | Global | Move the mouse cursor by 10px | `extensions/input/mouse_ext.py` |
| `D-U0-A-Space` / `U-U0-A-Space` | Global | Hold / release left mouse button | `extensions/input/mouse_ext.py` |
| `U0-A-PageUp` / `U0-A-PageDown` | Global | Mouse wheel up / down | `extensions/input/mouse_ext.py` |
| `Alt+U1+O` / `U1+Alt+O` | Global | Run `komorebic reload-configuration` | `kanata_config/win_to_f19.kbd` |
| `U1+I` / `U1+Q` / `U1+M` | Global | Open Python shortcuts palette / close window / minimize window | `kanata_config/win_to_f19.kbd` |
| `U1+H` / `U1+J` / `U1+K` / `U1+L` | Global | Focus window left / down / up / right in komorebi | `kanata_config/win_to_f19.kbd` |
| `Alt+U1+[` / `Alt+U1+]` / `U1+Alt+[` / `U1+Alt+]` | Global | Cycle komorebi focus backward / forward | `kanata_config/win_to_f19.kbd` |
| `Alt+U1+H` / `Alt+U1+J` / `Alt+U1+K` / `Alt+U1+L` / `Alt+U1+Enter` / `U1+Alt+H` / `U1+Alt+J` / `U1+Alt+K` / `U1+Alt+L` / `U1+Alt+Enter` | Global | Move window left / down / up / right or promote in komorebi | `kanata_config/win_to_f19.kbd` |
| `U1+Left` / `U1+Down` / `U1+Up` / `U1+Right` | Global | Stack window left / down / up / right in komorebi | `kanata_config/win_to_f19.kbd` |
| `U1+'` / `U1+[` / `U1+]` | Global | Unstack or cycle stack in komorebi | `kanata_config/win_to_f19.kbd` |
| `U1+=` / `U1+-` / `Alt+U1+=` / `Alt+U1+-` / `U1+Alt+=` / `U1+Alt+-` | Global | Resize komorebi container horizontally / vertically | `kanata_config/win_to_f19.kbd` |
| `U1+T` / `Alt+U1+F` / `Alt+U1+R` / `U1+P` / `U1+Alt+F` / `U1+Alt+R` | Global | Toggle float / monocle / retile / pause in komorebi | `kanata_config/win_to_f19.kbd` |
| `U1+X` / `U1+Y` | Global | Flip komorebi layout horizontally / vertically | `kanata_config/win_to_f19.kbd` |
| `U1+1..8` / `Alt+U1+1..8` / `U1+Alt+1..8` | Global | Focus workspace 0..7 or move window to workspace 0..7 in komorebi | `kanata_config/win_to_f19.kbd` |
| `U1+U2+0` / `U2+U1+0` | Global | Toggle bar visibility for monitor 0 | `kanata_config/win_to_f19.kbd` |
| `U1+U2+1` / `U2+U1+1` | Global | Toggle bar visibility for monitor 1 | `kanata_config/win_to_f19.kbd` |
| `H/J/K/L` in modal mode | Global | Focus window left / down / up / right in komorebi | `kanata_config/win_to_f19.kbd` |
| `Shift+H/J/K/L` in modal mode | Global | Move window left / down / up / right in komorebi | `kanata_config/win_to_f19.kbd` |
| `1..8` in modal mode | Global | Focus workspace 0..7 in komorebi | `kanata_config/win_to_f19.kbd` |
| `g-c-p` | Global / Coding apps | Type the preset git-commit phrase | `extensions/ui/coding_ext.py` |
| `g-p-p` | Global / Coding apps | Type the preset git-pull-merge-push phrase | `extensions/ui/coding_ext.py` |
| `s-p-7` / `s-p-5` | Global | Launch native `pwsh` / `powershell` | `extensions/ui/terminal_matrix_ext.py` |
| `r-p-7` / `r-p-5` | Global | Launch `rio` with `pwsh` / `powershell` | `extensions/ui/terminal_matrix_ext.py` |
| `g-p-7` / `g-p-5` | Global | Launch `ghostty` with `pwsh` / `powershell` | `extensions/ui/terminal_matrix_ext.py` |
| `f-n` | `texstudio.exe` | Paste `\Footnote{}` and move cursor left | `extensions/tex/texstudio_ext.py` |
| `U2-C` | `texstudio.exe` | Bracket-inner Copy (C-A-[ then C-C) | `extensions/tex/texstudio_ext.py` |
| `U2-D` | `texstudio.exe` | Bracket-outer Copy (C-A-] then C-C) | `extensions/tex/texstudio_ext.py` |
| `U2-X` | `texstudio.exe` | Bracket-inner Cut (C-A-[ then C-X) | `extensions/tex/texstudio_ext.py` |
| `U2-S` | `texstudio.exe` | Bracket-outer Cut (C-A-] then C-X) | `extensions/tex/texstudio_ext.py` |
| `U2-V` | `texstudio.exe` | Bracket-inner Paste (C-A-[ then C-V) | `extensions/tex/texstudio_ext.py` |
| `U2-F` | `texstudio.exe` | Bracket-outer Paste (C-A-] then C-V) | `extensions/tex/texstudio_ext.py` |
| `U0-W` | Global | Open the window switcher list with incremental search | `extensions/window/window_switcher.py` |

## List Window Controls

| Shortcut | Behavior | Scope |
| --- | --- | --- |
| `Ctrl+H` / `Ctrl+L` | Move to previous / next list | All Keyhac list windows |
| `Ctrl+J` / `Ctrl+K` | Move to next / previous item | All Keyhac list windows |
| `F` | Start incremental search | All Keyhac list windows |

## Keyhac U1 -> U2 Migration Check

This table covers only the Keyhac-owned `U1-*` bindings that were renamed to `U2-*`.
`U1+U2+*` combo intercepts are excluded because they are not simple prefix-only bindings.

| Current Keyhac binding | New binding | Scope | Behavior | Conflict? | Conflict source |
| --- | --- | --- | --- | --- | --- |
| `U1+C` | `U2+C` | `texstudio.exe` | Bracket-inner Copy | No | - |
| `U1+D` | `U2+D` | `texstudio.exe` | Bracket-outer Copy | No | - |
| `U1+X` | `U2+X` | `texstudio.exe` | Bracket-inner Cut | No | - |
| `U1+S` | `U2+S` | `texstudio.exe` | Bracket-outer Cut | No | - |
| `U1+V` | `U2+V` | `texstudio.exe` | Bracket-inner Paste | No | - |
| `U1+F` | `U2+F` | `texstudio.exe` | Bracket-outer Paste | No | - |

## Gaps

- Bare `U1+U2` / `U2+U1` currently has no action on either side; only `...+0` and `...+1` are defined.
