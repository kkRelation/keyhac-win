#Requires AutoHotkey v2.0
#SingleInstance Force
#Warn

SetWorkingDir A_ScriptDir
CoordMode "Mouse", "Screen"
CoordMode "ToolTip", "Screen"
CoordMode "Caret", "Screen"
#Include "core\modifiers.ahk"
#Include "core\powerkey_hint_gui.ahk"
#Include "core\powerkey.ahk"
#Include "extensions\clipboard\paste_text.ahk"
#Include "extensions\clipboard\selection_passthrough.ahk"
#Include "extensions\input\mouse.ahk"
#Include "extensions\input\native_passthrough.ahk"
#Include "extensions\system\copy_path.ahk"
#Include "extensions\system\terminal_matrix.ahk"
#Include "extensions\tex\texstudio_powerkey.ahk"
#Include "extensions\ui\snippet_sequences.ahk"
#Include "extensions\window\move_window.ahk"

; Kanata exports:
;   lmet   -> F19 -> U0
;   caps   -> F20 -> U1
;   ralt   -> F21 -> U2
;   rctrl  -> F22 -> U3
;   rshift -> F23 -> U4
^!r::Reload()

KH_InitUserModifiers()
KH_InitSelectionPassthroughExt()
KH_InitMouseExt()
KH_InitNativePassthroughExt()
KH_InitCopyPathExt()
KH_InitTerminalMatrixExt()
KH_InitTexstudioPowerKeyExt()
KH_InitMoveWindowExt()
KH_InitSnippetSequencesExt()
