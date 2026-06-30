#Requires AutoHotkey v2.0

global KH_ReloadStatusMarkerPath := A_Temp "\ahk-keyhac-reload.pending"
global KH_ReloadStatusFailureDelayMs := 3000
global KH_ReloadStatusHintMs := 3000

KH_InitReloadStatusExt() {
    global KH_ReloadStatusMarkerPath

    if !FileExist(KH_ReloadStatusMarkerPath) {
        return
    }

    try FileDelete(KH_ReloadStatusMarkerPath)
    SetTimer((*) => KH_ReloadStatus_Show("reload ahk", "success", "success"), -250)
}

KH_ReloadScript() {
    global KH_ReloadStatusMarkerPath, KH_ReloadStatusFailureDelayMs

    try FileDelete(KH_ReloadStatusMarkerPath)
    try FileAppend(A_Now, KH_ReloadStatusMarkerPath, "UTF-8")
    SetTimer(KH_ReloadStatus_AssumeFailed, -KH_ReloadStatusFailureDelayMs)

    try {
        Reload()
    } catch as err {
        try FileDelete(KH_ReloadStatusMarkerPath)
        KH_ReloadStatus_Show("reload ahk", "failed: " err.Message, "failure", 5000)
    }
}

KH_ReloadStatus_AssumeFailed() {
    global KH_ReloadStatusMarkerPath

    if !FileExist(KH_ReloadStatusMarkerPath) {
        return
    }

    try FileDelete(KH_ReloadStatusMarkerPath)
    KH_ReloadStatus_Show("reload ahk", "failed: old script is still running", "failure", 5000)
}

KH_ReloadStatus_Show(path, detail, style, timeoutMs := "") {
    global KH_PowerKeyHintGen, KH_ReloadStatusHintMs

    if timeoutMs = "" {
        timeoutMs := KH_ReloadStatusHintMs
    }

    KH_PowerKeyHintGen += 1
    gen := KH_PowerKeyHintGen

    ToolTip(, , , 19)
    MouseGetPos(&x, &y)
    KH_PowerKeyHintGui_ShowStyled(path, detail, x + 75, y - 8, style)
    SetTimer((*) => KH_PowerKey_HideHintIfCurrent(gen), -timeoutMs)
}
