#Requires AutoHotkey v2.0

KH_InitTexstudioBracketsExt() {
    winTitle := "ahk_exe texstudio.exe"

    KH_Bind("U2-C", (*) => KH_TexstudioBracketThen("^![", "^c"), "On", winTitle)
    KH_Bind("U2-D", (*) => KH_TexstudioBracketThen("^!]", "^c"), "On", winTitle)
    KH_Bind("U2-X", (*) => KH_TexstudioBracketThen("^![", "^x"), "On", winTitle)
    KH_Bind("U2-S", (*) => KH_TexstudioBracketThen("^!]", "^x"), "On", winTitle)
    KH_Bind("U2-V", (*) => KH_TexstudioBracketThen("^![", "^v"), "On", winTitle)
    KH_Bind("U2-F", (*) => KH_TexstudioBracketThen("^!]", "^v"), "On", winTitle)
}

KH_TexstudioBracketThen(bracketKeys, followupKeys, delayMs := 200) {
    SendEvent(bracketKeys)
    SetTimer((*) => SendEvent(followupKeys), -delayMs)
}
