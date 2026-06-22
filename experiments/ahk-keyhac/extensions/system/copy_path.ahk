KH_InitCopyPathExt() {
    KH_Bind("U0-C", (*) => KH_CopyPathOrCopy())
}

KH_CopyPathOrCopy() {
    try {
        processName := StrLower(WinGetProcessName("A"))
    } catch {
        processName := ""
    }

    if KH_IsPathCopyTerminal(processName) {
        KH_CopyTerminalCurrentPath(processName)
        return
    }

    Send("!d")
    Sleep(30)
    Send("^c")
}

KH_IsPathCopyTerminal(processName) {
    terminalNames := Map(
        "wt.exe", true,
        "windowsterminal.exe", true,
        "rio.exe", true,
        "ghostty.exe", true,
        "cmd.exe", true,
        "powershell.exe", true,
        "pwsh.exe", true,
    )
    return terminalNames.Has(processName)
}

KH_CopyTerminalCurrentPath(processName) {
    if processName = "cmd.exe" {
        commandText := 'powershell -NoProfile -Command "(Get-Location).Path | Set-Clipboard"'
    } else {
        commandText := "(Get-Location).Path | Set-Clipboard"
    }

    SendText(commandText)
    SetTimer((*) => Send("{Enter}"), -100)
}
