# KKK

KKK = Kanata + Keyhac + Komorebi.

## Layering

- Kanata owns physical-key interception, layer routing, and multi-mod printable combos.
- Keyhac owns Python workflows, shared state, list UI, launchers, and app-specific logic.
- Komorebi owns the actual window-manager side effects and bar visibility state.

## Declarative Source

- Source of truth: `scripts/kkk_declarative.py` in the keyhac repo.
- Generator: `scripts/generate_kkk_bindings.py` in the keyhac repo.
- Generated exports:
  - `extension/generated_kkk_bindings.py`
  - `generated_kkk_bindings.kbd` in the kanata_config repo

## Current Patterns

- modifier-export `u0`: `lmet` -> `f19` -> `U0`
- modifier-export `u1`: `caps` -> `f20` -> `U1`
- modifier-export `u2`: `ralt` -> `f21` -> `U2`
- modifier-export `u3`: `rctrl` -> `f22` -> `U3`
- modifier-export `u4`: `rshift` -> `f23` -> `U4`
- state-sync `komorebi_modal_sync`: `kanata` owns modal state and updates shared state through `D:\C2D\Desktop\Code\Python\automation\state_center\target\release\state-client.exe`.
- direct-command `km_toggle_modal`: `Ctrl+Caps` / `Caps+Ctrl` toggles Kanata's `base/modal` layer and writes shared modal state.
- direct-command `km_focus_left`: modal `h` runs `focus left`.
- direct-command `km_focus_down`: modal `j` runs `focus down`.
- direct-command `km_focus_up`: modal `k` runs `focus up`.
- direct-command `km_focus_right`: modal `l` runs `focus right`.
- direct-command `km_core_caps_actions`: `Pure U1-* window-management bindings are Kanata-owned.`
- direct-command `km_core_alt_caps_actions`: `Pure A-U1-* window-management bindings are Kanata-owned.`
- direct-command `km_core_modal_shift_actions`: `Pure D-S-* modal window-management bindings are Kanata-owned.`
- combo-intercept `bar_toggle_0`: `u1+u2+0` is Kanata-owned and runs `native_exe` directly.
- combo-intercept `bar_toggle_1`: `u1+u2+1` is Kanata-owned and runs `native_exe` directly.

## Ownership Summary

- Default KKK runtime backend: `kanata`.
- Kanata owns simple komorebi chords and direct commands; Keyhac owns Python/UI/stateful workflows.
- Bare `U1+U2` / `U2+U1` intentionally has no action.

## Expansion Rule

- For `u3/u4/u5 + printable key`, prefer Kanata combo interception.
- If the action is short and stateless, let Kanata run it directly.
- If the action needs Python/UI/state, let Kanata emit a stable signal and let Keyhac handle it.

## Project Note

- This copy lives in the `keyhac` repo as a local reading guide.
