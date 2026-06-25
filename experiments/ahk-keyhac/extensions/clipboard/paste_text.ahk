#Requires AutoHotkey v2.0

KH_MakePasteTextCommand(text, postKeys := [], pasteDelayMs := 100, restoreDelayMs := 200) {
    running := false
    command := (*) => KH_RunPasteTextCommand(&running, text, postKeys, pasteDelayMs, restoreDelayMs)
    return command
}

KH_RunPasteTextCommand(&running, text, postKeys, pasteDelayMs, restoreDelayMs) {
    if running {
        return
    }

    running := true
    KH_PasteTextAndRestore(text, postKeys, pasteDelayMs, restoreDelayMs, () => running := false)
}

KH_PasteTextAndRestore(text, postKeys, pasteDelayMs, restoreDelayMs, onDone) {
    previousClipboard := A_Clipboard
    A_Clipboard := text

    doPaste := (*) => KH_DoPasteText(previousClipboard, postKeys, pasteDelayMs, restoreDelayMs, onDone)
    SetTimer(doPaste, -pasteDelayMs)
}

KH_DoPasteText(previousClipboard, postKeys, pasteDelayMs, restoreDelayMs, onDone) {
    SendEvent "^v"

    if postKeys.Length {
        sendPostKeys := (*) => KH_SendPostKeys(postKeys)
        SetTimer(sendPostKeys, -pasteDelayMs)
    }

    restoreClipboard := (*) => KH_RestoreClipboard(previousClipboard, onDone)
    SetTimer(restoreClipboard, -restoreDelayMs)
}

KH_SendPostKeys(postKeys) {
    for key in postKeys {
        sendName := KH_PowerKey_KeyToHotkey(key)
        SendEvent "{" sendName "}"
    }
}

KH_RestoreClipboard(previousClipboard, onDone) {
    A_Clipboard := previousClipboard
    onDone.Call()
}
