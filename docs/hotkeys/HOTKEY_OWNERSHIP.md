# Hotkey Ownership

This file is the practical KKK ownership map for the current setup.

## Rule

- Kanata owns simple chords and direct command execution.
- Keyhac owns Python workflows, UI, shared state publishing, and app-specific logic.
- Bare `U1+U2` / `U2+U1` intentionally has no action.

## Kanata-Owned

| Shortcut group | Behavior | Source |
| --- | --- | --- |
| `U1+A` | Send native `CapsLock` | `kanata_config/win_to_f19.kbd` |
| `U0+Alt` | Send native `LWin` | `kanata_config/win_to_f19.kbd` |
| `Ctrl+U1` / `U1+Ctrl` | Toggle `base/modal` and sync modal state | `kanata_config/win_to_f19.kbd` |
| `U1+I` | Launch komorebi shortcuts UI | `kanata_config/win_to_f19.kbd` |
| `U1+Q` / `U1+M` | Close / minimize window | `kanata_config/win_to_f19.kbd` |
| `U1+H/J/K/L` | Focus window left / down / up / right | `kanata_config/win_to_f19.kbd` |
| `Alt+U1+H/J/K/L` / `Alt+U1+Tnter` | Move window or promote | `kanata_config/win_to_f19.kbd` |
| `U1+Left/Down/Up/Right` | Stack window left / down / up / right | `kanata_config/win_to_f19.kbd` |
| `U1+'` / `U1+[` / `U1+]` | Unstack / cycle stack | `kanata_config/win_to_f19.kbd` |
| `U1+,` / `U1+.` | Cycle layout previous / next | `kanata_config/win_to_f19.kbd` |
| `Alt+U1+,` / `Alt+U1+.` | Change layout to grid / bsp | `kanata_config/win_to_f19.kbd` |
| `U1+=` / `U1+-` | Resize horizontally | `kanata_config/win_to_f19.kbd` |
| `Alt+U1+=` / `Alt+U1+-` | Resize vertically | `kanata_config/win_to_f19.kbd` |
| `U1+T/P/X/Y` | Toggle float / pause / flip layout | `kanata_config/win_to_f19.kbd` |
| `Alt+U1+F/R/O/G/[ / ]` | Monocle / retile / reload / unstack-all / cycle focus | `kanata_config/win_to_f19.kbd` |
| `U1+1..9` / `Alt+U1+1..9` | Focus workspace / move to workspace | `kanata_config/win_to_f19.kbd` |
| `U1+U2+0` / `U1+U2+1` | Toggle bar visibility for monitor 0 / 1 | `kanata_config/win_to_f19.kbd` |
| Modal `H/J/K/L`, `Shift+H/J/K/L`, `1..9`, `Shift+1..9`, `Shift+Enter`, `Shift+O`, `Shift+-`, `Shift+=` | Modal focus / move / workspace / resize / reload commands | `kanata_config/win_to_f19.kbd` |

## Keyhac-Owned

| Shortcut group | Behavior | Source |
| --- | --- | --- |
| `C-A-S-7/8/9/0/-` | Toggle `U2/U3/U4/U0/U1` modifier export modes | `custom_config/main.py` |
| `C-S-A-U` | Toggle all five exported modifier modes | `custom_config/main.py` |
| `U1+;` | Open clipboard history list | `custom_config/main.py` |
| `U0+0` / `U0+3` | Toggle / play recorded macro | `custom_config/main.py` |
| `U0+C` | In PowerShell terminal copy current path; otherwise fallback copy selection | `custom_config/main.py` |
| `U0+Left/Right/Up/Down` | Move active window by 10px | `custom_config/main.py` |
| `U0+Space` | Open application launcher list | `extensions/apps/app_launcher.py` |
| `U0+A` | Copy selection first, then pass through `Alt+Left` | `extensions/clipboard/clipboard_ext.py` |
| `U0+Alt+Left/Right/Up/Down` | Move mouse cursor | `extensions/input/mouse_ext.py` |
| `D-U0-A-Space` / `U-U0-A-Space` | Hold / release left mouse button | `extensions/input/mouse_ext.py` |
| `U0-A-PageUp/PageDown` | Mouse wheel up / down | `extensions/input/mouse_ext.py` |
| `g-c-p` / `g-p-p` / `g-l-c` | Insert git workflow snippets | `extensions/ui/snippet_sequences.py` |
| `U0-W` | Open window switcher list with incremental search | `extensions/window/window_switcher.py` |
| `s-p-7` / `s-p-5` | Launch native `pwsh` / `powershell` | `extensions/ui/terminal_matrix_ext.py` |
| `r-p-7` / `r-p-5` | Launch `rio` with `pwsh` / `powershell` | `extensions/ui/terminal_matrix_ext.py` |
| `g-p-7` / `g-p-5` | Launch `ghostty` with `pwsh` / `powershell` | `extensions/ui/terminal_matrix_ext.py` |
| `f-n` in `texstudio.exe` | Insert `\\Footnote{}` wrapper | `extensions/tex/texstudio_ext.py` |
| `n-b`, `m-r`, `p-l`, `p-g`, `g-r`, `b-l` in `texstudio.exe` | Insert TeX color wrappers | `extensions/tex/texstudio_ext.py` |
| `U2-C/D/X/S/V/F` in `texstudio.exe` | Bracket copy / cut / paste helpers | `extensions/tex/texstudio_ext.py` |

## List Window Controls

| Shortcut | Behavior |
| --- | --- |
| `Ctrl+H` / `Ctrl+L` | Move to previous / next list |
| `Ctrl+J` / `Ctrl+K` | Move to next / previous item |
| `F` | Start incremental search |

## U1 -> U2 Migration Check

This is the Keyhac-owned Texstudio subset only. `U1+U2+*` combos are excluded because they are not simple prefix-only bindings.

| Current Keyhac binding | New binding | Scope | Conflict? | Conflict source |
| --- | --- | --- | --- | --- |
| `U1+C` | `U2+C` | `texstudio.exe` | No | - |
| `U1+D` | `U2+D` | `texstudio.exe` | No | - |
| `U1+X` | `U2+X` | `texstudio.exe` | No | - |
| `U1+S` | `U2+S` | `texstudio.exe` | No | - |
| `U1+V` | `U2+V` | `texstudio.exe` | No | - |
| `U1+F` | `U2+F` | `texstudio.exe` | No | - |

## Notes

- Keyhac still publishes shared state such as modifier labels and modal colors.
- Keyhac no longer owns pure komorebi movement/layout/stack/workspace shortcuts in the default KKK path.
- Recovery entrypoint is external: rerun Keyhac via `tools/dev/run_keyhac.ps1` (for example from Quicker), not via an in-Keyhac hotkey.
