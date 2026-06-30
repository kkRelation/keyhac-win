#Requires AutoHotkey v2.0

global KH_PowerKeyHintGui := ""
global KH_PowerKeyHintPathCtrl := ""
global KH_PowerKeyHintDetailCtrl := ""
global KH_PowerKeyHintGuiCharWidth := 8
global KH_PowerKeyHintGuiLineHeight := 18
global KH_PowerKeyHintGuiOpacity := 218

KH_PowerKeyHintGui_Show(path, detail, x, y) {
    KH_PowerKeyHintGui_ShowStyled(path, detail, x, y, "powerkey")
}

KH_PowerKeyHintGui_ShowStyled(path, detail, x, y, style := "powerkey") {
    global KH_PowerKeyHintGui, KH_PowerKeyHintPathCtrl, KH_PowerKeyHintDetailCtrl, KH_PowerKeyHintGuiOpacity

    KH_PowerKeyHintGui_Ensure()
    styleSpec := KH_PowerKeyHintGui_Style(style)
    detail := KH_PowerKeyHintGui_IndentDetail(path, detail)
    width := KH_PowerKeyHintGui_TextWidth(path, detail)

    KH_PowerKeyHintGui.BackColor := styleSpec.back
    KH_PowerKeyHintPathCtrl.Opt("c" styleSpec.pathText " Background" styleSpec.pathBg)
    KH_PowerKeyHintDetailCtrl.Opt("c" styleSpec.detailText " Background" styleSpec.back)
    KH_PowerKeyHintPathCtrl.Text := path
    KH_PowerKeyHintDetailCtrl.Text := detail
    KH_PowerKeyHintPathCtrl.Move(, , width)
    KH_PowerKeyHintDetailCtrl.Move(, , width)

    KH_PowerKeyHintGui.Show("NA AutoSize x" x " y" y)
    try WinSetExStyle("+0x20", "ahk_id " KH_PowerKeyHintGui.Hwnd)
    try WinSetTransparent(styleSpec.opacity, "ahk_id " KH_PowerKeyHintGui.Hwnd)
}

KH_PowerKeyHintGui_Hide() {
    global KH_PowerKeyHintGui

    if KH_PowerKeyHintGui != "" {
        KH_PowerKeyHintGui.Hide()
    }
}

KH_PowerKeyHintGui_Ensure() {
    global KH_PowerKeyHintGui, KH_PowerKeyHintPathCtrl, KH_PowerKeyHintDetailCtrl

    if KH_PowerKeyHintGui != "" {
        return
    }

    KH_PowerKeyHintGui := Gui("-Caption +AlwaysOnTop +ToolWindow +E0x20 -DPIScale", "AHK Keyhac PowerKey Hint")
    KH_PowerKeyHintGui.MarginX := 8
    KH_PowerKeyHintGui.MarginY := 6
    KH_PowerKeyHintGui.BackColor := "20242A"

    KH_PowerKeyHintGui.SetFont("s10 w700 cF3F4F6 q5", "Cascadia Mono")
    KH_PowerKeyHintPathCtrl := KH_PowerKeyHintGui.AddText("xm ym w320 cF3F4F6 Background303846", "")

    KH_PowerKeyHintGui.SetFont("s10 w400 cD5D8DF q5", "Cascadia Mono")
    KH_PowerKeyHintDetailCtrl := KH_PowerKeyHintGui.AddText("xm y+5 w320 cD5D8DF Background20242A", "")
}

KH_PowerKeyHintGui_IndentDetail(path, detail) {
    if detail = "" {
        return ""
    }

    indent := StrRepeat(" ", StrLen(path) + 2)
    result := ""
    for line in StrSplit(detail, "`n") {
        result .= indent line "`n"
    }
    return RTrim(result, "`n")
}

KH_PowerKeyHintGui_TextWidth(path, detail) {
    global KH_PowerKeyHintGuiCharWidth

    maxChars := StrLen(path)
    for line in StrSplit(detail, "`n") {
        maxChars := Max(maxChars, StrLen(line))
    }
    return Max(80, (maxChars + 2) * KH_PowerKeyHintGuiCharWidth)
}

KH_PowerKeyHintGui_Style(style) {
    global KH_PowerKeyHintGuiOpacity

    switch style {
        case "success":
            return {
                back: "0E1F17",
                pathBg: "14532D",
                pathText: "DCFCE7",
                detailText: "BBF7D0",
                opacity: 232
            }
        case "failure":
            return {
                back: "271111",
                pathBg: "7F1D1D",
                pathText: "FEE2E2",
                detailText: "FECACA",
                opacity: 238
            }
        default:
            return {
                back: "20242A",
                pathBg: "303846",
                pathText: "F3F4F6",
                detailText: "D5D8DF",
                opacity: KH_PowerKeyHintGuiOpacity
            }
    }
}
