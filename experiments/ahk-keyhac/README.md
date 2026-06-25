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

`core/powerkey.ahk` provides the initial PowerKey sequence engine for later
snippet, terminal-matrix, and app-specific sequence migrations. The first
version supports plain prefix/suffix key sequences via `InputHook`; it does
not yet implement Keyhac's full key-up trigger and flusher behavior.

Currently migrated local-only bindings:

- `Ctrl+Alt+R`: reload this AHK script.
- `U0-C`: in supported terminals, copy the current working directory to the
  clipboard by typing a shell command and pressing Enter after a short delay;
  otherwise fall back to `Alt+D`, then `Ctrl+C`.
- `U0-A`: probe-copy the current selection, then pass through `Alt+L`.
- `U0-Left/Right/Up/Down`: move the mouse cursor by 10 px.
- `D-U0-Space` / `U-U0-Space`: hold / release the left mouse button.
- `U0-PageUp/PageDown`: mouse wheel up / down.
- `U0-Home/End`: mouse horizontal wheel left / right.
- `U0+Alt` alone: restore native `LWin` tap behavior while leaving
  `U0+Alt+other-key` passthrough intact.
- `C-U0-Left/Right/Up/Down`: move the active window by 10 px.

Do not port Keyhac's bundled sample bindings unless the local `keyhac` or
`keyhac-win` configuration changed their behavior. For example, the virtual
mouse bindings under `U0-A-*` already exist in the upstream
`keyhac_183/keyhac/_config.py` sample. This prototype intentionally remaps
that mouse layer from `U0-A-*` to plain `U0-*` to preserve Kanata's
`U0+Alt => LWin` behavior.
