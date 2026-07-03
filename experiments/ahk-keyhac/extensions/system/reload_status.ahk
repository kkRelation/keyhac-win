#Requires AutoHotkey v2.0

global KH_ReloadStatusMarkerPath := A_Temp "\ahk-keyhac-reload.pending"
global KH_ReloadStatusFailureDelayMs := 3000
global KH_ReloadStatusHintMs := 3000

KH_InitReloadStatusExt() {
    global KH_ReloadStatusMarkerPath

    if !FileExist(KH_ReloadStatusMarkerPath) {
        return
    }

    action := KH_ReloadStatus_ReadPendingAction()
    try FileDelete(KH_ReloadStatusMarkerPath)
    if action = "reboot" {
        SetTimer((*) => KH_ReloadStatus_Show("AHK", "rebooted.", "reboot"), -250)
    } else {
        SetTimer((*) => KH_ReloadStatus_Show("AHK", "reloaded.", "success"), -250)
    }
}

KH_ReloadScript() {
    global KH_ReloadStatusMarkerPath, KH_ReloadStatusFailureDelayMs

    KH_ReloadStatus_WritePendingAction("reload")
    SetTimer(KH_ReloadStatus_AssumeFailed, -KH_ReloadStatusFailureDelayMs)

    try {
        Reload()
    } catch as err {
        try FileDelete(KH_ReloadStatusMarkerPath)
        KH_ReloadStatus_Show("reload ahk", "failed: " err.Message, "failure", 5000)
    }
}

KH_RestartScriptViaLauncher() {
    global KH_ReloadStatusMarkerPath, KH_ReloadStatusFailureDelayMs

    launcherPath := A_ScriptDir "\run-ahk-keyhac-hidden.vbs"
    if !FileExist(launcherPath) {
        KH_ReloadStatus_Show("restart ahk", "failed: launcher not found", "failure", 5000)
        return
    }

    KH_ReloadStatus_WritePendingAction("reboot")
    SetTimer(KH_ReloadStatus_AssumeFailed, -KH_ReloadStatusFailureDelayMs)

    try {
        Run(A_WinDir "\System32\wscript.exe //B `"" launcherPath "`"")
    } catch as err {
        try FileDelete(KH_ReloadStatusMarkerPath)
        KH_ReloadStatus_Show("restart ahk", "failed: " err.Message, "failure", 5000)
    }
}

KH_ReloadStatus_AssumeFailed() {
    global KH_ReloadStatusMarkerPath

    if !FileExist(KH_ReloadStatusMarkerPath) {
        return
    }

    action := KH_ReloadStatus_ReadPendingAction()
    try FileDelete(KH_ReloadStatusMarkerPath)
    path := action = "reboot" ? "reboot ahk" : "reload ahk"
    KH_ReloadStatus_Show(path, "failed: old script is still running", "failure", 5000)
}

KH_ReloadStatus_WritePendingAction(action) {
    global KH_ReloadStatusMarkerPath

    try FileDelete(KH_ReloadStatusMarkerPath)
    try FileAppend(action "`n" A_Now, KH_ReloadStatusMarkerPath, "UTF-8")
}

KH_ReloadStatus_ReadPendingAction() {
    global KH_ReloadStatusMarkerPath

    try {
        content := FileRead(KH_ReloadStatusMarkerPath, "UTF-8")
        firstLine := StrSplit(Trim(content, "`r`n`t "), "`n", "`r", 2)[1]
        if firstLine = "reboot" {
            return "reboot"
        }
    }
    return "reload"
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
