#Requires AutoHotkey v2.0
#SingleInstance Force
#Warn

SetWorkingDir A_ScriptDir
#Include "core\modifiers.ahk"

; Kanata exports:
;   lmet   -> F19 -> U0
;   caps   -> F20 -> U1
;   ralt   -> F21 -> U2
;   rctrl  -> F22 -> U3
;   rshift -> F23 -> U4
KH_InitUserModifiers()

; Smoke-test bindings. Replace these with real migrated keyhac-win actions as
; modules are ported.
KH_Bind("U0-W", (*) => ToolTipFor("U0-W"))
KH_Bind("U1-Space", (*) => ToolTipFor("U1-Space"))
KH_Bind("U2-C", (*) => ToolTipFor("U2-C"))
KH_Bind("U3-J", (*) => ToolTipFor("U3-J"))
KH_Bind("U4-K", (*) => ToolTipFor("U4-K"))

ToolTipFor(label) {
    ToolTip label
    SetTimer () => ToolTip(), -700
}
