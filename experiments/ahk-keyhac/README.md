# AHK Keyhac Prototype

This is a small AutoHotkey v2 prototype for testing the Kanata-to-Keyhac
modifier export model.

Kanata currently exports the five user modifiers as function keys:

| Keyhac label | Kanata source | AHK-visible key |
| --- | --- | --- |
| U0 | lmet | F19 |
| U1 | caps | F20 |
| U2 | ralt | F21 |
| U3 | rctrl | F22 |
| U4 | rshift | F23 |

Run:

```powershell
& 'C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe' '.\experiments\ahk-keyhac\KeyhacAhk.ahk'
```

The important part is `core/modifiers.ahk`, which exposes
`KH_Bind("U1-W", callback)` for Keyhac-style migration work.

`core/powerkey.ahk` provides the initial PowerKey sequence engine for snippet,
terminal-matrix, and app-specific sequence migrations. It uses a Keyhac-style
down/up dispatcher with context-only flusher hotkeys, replaying cancelled text
prefixes as key events so IME composition can continue. The tap/continuation
timeout is 50ms. Active sequences show a lightweight caret/mouse `ToolTip`
or GUI hint with the current key path and next candidates. The default GUI
backend uses a small non-activating, click-through window with a mono font and
a distinct first-line style; the ToolTip backend remains available as fallback.
Hint updates use a three-second debounce: each sequence progress, match, or
no-match update resets the timer.

Currently migrated local-only bindings:

- `Ctrl+Alt+R`: reload this AHK script and show a compact success/failure hint.
- `g c-p`, `g p-p`, `g l-c`: paste the migrated git prompt snippets.
- `s p-7`, `s p-5`: launch Windows Terminal with PowerShell 7 / 5.
- `r p-7`, `r p-5`: launch Rio with PowerShell 7 / 5.
- `g p-7`, `g p-5`: launch Ghostty with PowerShell 7 / 5.
- In TeXstudio: `f n`, `n b`, `m r`, `p l`, `p g`, `g r`, `b l`
  insert or wrap TeX snippets/colors.
- In TeXstudio: `U2-C/D/X/S/V/F` run TeXstudio bracket selection helpers
  followed by copy/cut/paste.
- `U0-C`: in supported terminals, copy the current working directory to the
  clipboard by typing a shell command and pressing Enter after a short delay;
  otherwise fall back to `Alt+D`, then `Ctrl+C`.
- `U0-A`: probe-copy the current selection, then pass through `Alt+L`.
- `U0-Left/Right/Up/Down`: move the mouse cursor by 10 px.
- `D-U0-Space` / `U-U0-Space`: hold / release the left mouse button.
- `U0-PageUp/PageDown`: mouse wheel up / down.
- `U0-Home/End`: mouse horizontal wheel left / right.
- `C-U0-PageUp/PageDown/Home/End`: mouse wheel up / down / left / right by 5 notches.
- `C-S-U0-PageUp/PageDown/Home/End`: mouse wheel up / down / left / right by 20 notches.
- `U0+Alt` alone: restore native `LWin` tap behavior while leaving
  `U0+Alt+other-key` passthrough intact.
- `C-U0-Left/Right/Up/Down`: move the active window by 10 px.

Do not port Keyhac's bundled sample bindings unless the local `keyhac` or
`keyhac-win` configuration changed their behavior. For example, the virtual
mouse bindings under `U0-A-*` already exist in the upstream
`keyhac_183/keyhac/_config.py` sample. This prototype intentionally remaps
that mouse layer from `U0-A-*` to plain `U0-*` to preserve Kanata's
`U0+Alt => LWin` behavior.
