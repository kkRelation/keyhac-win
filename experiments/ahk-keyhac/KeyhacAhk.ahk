#Requires AutoHotkey v2.0
#SingleInstance Force
#Warn

SetWorkingDir A_ScriptDir
#Include "core\modifiers.ahk"
#Include "extensions\input\mouse.ahk"
#Include "extensions\input\native_passthrough.ahk"
#Include "extensions\system\copy_path.ahk"

; Kanata exports:
;   lmet   -> F19 -> U0
;   caps   -> F20 -> U1
;   ralt   -> F21 -> U2
;   rctrl  -> F22 -> U3
;   rshift -> F23 -> U4
KH_InitUserModifiers()
KH_InitMouseExt()
KH_InitNativePassthroughExt()
KH_InitCopyPathExt()
