#Requires AutoHotkey v2.0

global KH_TexstudioSmartInsertRunning := false

KH_InitTexstudioPowerKeyExt() {
    scopeName := "exe:texstudio.exe"
    winTitle := "ahk_exe texstudio.exe"

    KH_PowerKey_Add("f", "n", KH_MakeTexstudioSmartInsertCommand("\Footnote{", "}"), scopeName, winTitle, "insert/wrap \Footnote{}")
    KH_PowerKey_Add("n", "b", KH_MakeTexstudioColorCommand("NavyBlue"), scopeName, winTitle, "insert/wrap \textcolor{NavyBlue}{}")
    KH_PowerKey_Add("m", "r", KH_MakeTexstudioColorCommand("Maroon"), scopeName, winTitle, "insert/wrap \textcolor{Maroon}{}")
    KH_PowerKey_Add("p", "l", KH_MakeTexstudioColorCommand("Plum"), scopeName, winTitle, "insert/wrap \textcolor{Plum}{}")
    KH_PowerKey_Add("p", "g", KH_MakeTexstudioColorCommand("PineGreen"), scopeName, winTitle, "insert/wrap \textcolor{PineGreen}{}")
    KH_PowerKey_Add("g", "r", KH_MakeTexstudioColorCommand("Gray"), scopeName, winTitle, "insert/wrap \textcolor{Gray}{}")
    KH_PowerKey_Add("b", "l", KH_MakeTexstudioColorCommand("Black"), scopeName, winTitle, "insert/wrap \textcolor{Black}{}")
}

KH_MakeTexstudioColorCommand(colorName) {
    return KH_MakeTexstudioSmartInsertCommand("\textcolor{" colorName "}{", "}")
}

KH_MakeTexstudioSmartInsertCommand(prefix, suffix) {
    return (*) => KH_TexstudioSmartInsert(prefix, suffix)
}

KH_TexstudioSmartInsert(prefix, suffix) {
    global KH_TexstudioSmartInsertRunning

    if KH_TexstudioSmartInsertRunning {
        return
    }
    KH_TexstudioSmartInsertRunning := true

    previousClipboard := A_Clipboard
    sentinel := Chr(0) "__KH_TEX_SENTINEL__" Chr(0)
    A_Clipboard := sentinel

    startTick := A_TickCount
    doCopy := (*) => SendEvent("^c")
    pollClipboard := ""
    pollClipboard := (*) => KH_TexstudioPollSelection(
        prefix,
        suffix,
        sentinel,
        previousClipboard,
        startTick,
        pollClipboard
    )

    SetTimer(doCopy, -30)
    SetTimer(pollClipboard, -45)
}

KH_TexstudioPollSelection(prefix, suffix, sentinel, previousClipboard, startTick, pollClipboard) {
    global KH_TexstudioSmartInsertRunning

    clipboardText := A_Clipboard
    if clipboardText != "" && clipboardText != sentinel {
        KH_TexstudioPasteAndRestore(prefix clipboardText suffix, previousClipboard, [])
        KH_TexstudioSmartInsertRunning := false
        return
    }

    if A_TickCount - startTick >= 300 {
        postKeys := []
        Loop StrLen(suffix) {
            postKeys.Push("left")
        }
        KH_TexstudioPasteAndRestore(prefix suffix, previousClipboard, postKeys)
        KH_TexstudioSmartInsertRunning := false
        return
    }

    SetTimer(pollClipboard, -15)
}

KH_TexstudioPasteAndRestore(text, previousClipboard, postKeys) {
    A_Clipboard := text

    doPaste := (*) => KH_TexstudioDoPaste(previousClipboard, postKeys)
    SetTimer(doPaste, -80)
}

KH_TexstudioDoPaste(previousClipboard, postKeys) {
    SendEvent("^v")

    if postKeys.Length {
        sendPostKeys := (*) => KH_SendPostKeys(postKeys)
        SetTimer(sendPostKeys, -80)
    }

    restoreClipboard := (*) => KH_TexstudioRestoreClipboard(previousClipboard)
    SetTimer(restoreClipboard, -180)
}

KH_TexstudioRestoreClipboard(previousClipboard) {
    A_Clipboard := previousClipboard
}
