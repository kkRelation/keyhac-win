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

The current entry script registers smoke-test bindings such as `U0-W`,
`U1-Space`, and `U2-C`; each shows a tooltip. The important part is
`core/modifiers.ahk`, which exposes `KH_Bind("U1-W", callback)` for later
Keyhac-style migration work.
