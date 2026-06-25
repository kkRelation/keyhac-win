#Requires AutoHotkey v2.0

global KH_PS5_PROFILE_PATH := "D:\C2D\Documents\WindowsPowerShell\profile.ps1"
global KH_WT_PROFILE_BY_SHELL := Map(
    "ps7", "{9f986cf1-261a-4f88-9f66-a2d0ce5f4b8e}",
    "ps5", "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}"
)
global KH_GHOSTTY_CONFIG_PATH := "E:\MCP\Projects\ghostty-windows\config\config"
global KH_GHOSTTY_CONFIG_BY_SHELL := Map(
    "ps5", "E:\MCP\Projects\ghostty-windows\config\config.ps5",
    "ps7", "E:\MCP\Projects\ghostty-windows\config\config.ps7"
)
global KH_RIO_CONFIG_HOME := "D:\C2D\dotfiles\rio"
global KH_RIO_CONFIG_PATH := KH_RIO_CONFIG_HOME "\config.toml"

KH_InitTerminalMatrixExt() {
    KH_PowerKey_AddMany("s", Map(
        "p-7", (*) => KH_LaunchTerminal("native", "ps7"),
        "p-5", (*) => KH_LaunchTerminal("native", "ps5")
    ))
    KH_PowerKey_AddMany("r", Map(
        "p-7", (*) => KH_LaunchTerminal("rio", "ps7"),
        "p-5", (*) => KH_LaunchTerminal("rio", "ps5")
    ))
    KH_PowerKey_AddMany("g", Map(
        "p-7", (*) => KH_LaunchTerminal("ghostty", "ps7"),
        "p-5", (*) => KH_LaunchTerminal("ghostty", "ps5")
    ))
}

KH_LaunchTerminal(terminalKind, shellKind) {
    launchDir := KH_GetExplorerPath()
    if launchDir = "" {
        launchDir := EnvGet("USERPROFILE")
    }
    if launchDir = "" {
        launchDir := A_ScriptDir
    }

    KH_RememberPathForZoxide(launchDir)

    try {
        if terminalKind = "native" {
            KH_LaunchNativeTerminal(shellKind, launchDir)
        } else if terminalKind = "rio" {
            KH_LaunchRio(shellKind, launchDir)
        } else if terminalKind = "ghostty" {
            KH_LaunchGhostty(shellKind, launchDir)
        }
    } catch as err {
        MsgBox("Terminal launch failed: " terminalKind "/" shellKind "`n" err.Message, "AHK Keyhac")
    }
}

KH_GetExplorerPath() {
    try {
        hwnd := WinGetID("A")
        processName := StrLower(WinGetProcessName("ahk_id " hwnd))
        if processName != "explorer.exe" {
            return ""
        }

        shell := ComObject("Shell.Application")
        for window in shell.Windows {
            try {
                if window.HWND = hwnd {
                    path := window.Document.Folder.Self.Path
                    if DirExist(path) {
                        return path
                    }
                }
            }
        }
    }
    return ""
}

KH_RememberPathForZoxide(path) {
    if !FileExist(path) {
        return
    }

    try {
        Run(KH_JoinCommand(["zoxide", "add", path]), , "Hide")
    }
}

KH_LaunchNativeTerminal(shellKind, launchDir) {
    global KH_WT_PROFILE_BY_SHELL

    profile := KH_WT_PROFILE_BY_SHELL.Has(shellKind) ? KH_WT_PROFILE_BY_SHELL[shellKind] : ""
    shellArgs := KH_GetShellArgs(shellKind)
    if profile != "" {
        command := KH_JoinCommand(["wt", "new-tab", "-p", profile, "-d", launchDir])
            . " " KH_JoinCommand(shellArgs)
        Run(command, launchDir)
        return
    }

    Run(KH_JoinCommand(shellArgs), launchDir)
}

KH_LaunchRio(shellKind, launchDir) {
    global KH_RIO_CONFIG_HOME, KH_RIO_CONFIG_PATH

    previousConfigHome := EnvGet("RIO_CONFIG_HOME")
    previousConfig := EnvGet("RIO_CONFIG")
    EnvSet("RIO_CONFIG_HOME", KH_RIO_CONFIG_HOME)
    EnvSet("RIO_CONFIG", KH_RIO_CONFIG_PATH)
    try {
        command := KH_JoinCommand(["rio", "-w", launchDir, "-e"]) " " KH_JoinCommand(KH_GetShellArgs(shellKind))
        Run(command, launchDir)
    } finally {
        EnvSet("RIO_CONFIG_HOME", previousConfigHome)
        EnvSet("RIO_CONFIG", previousConfig)
    }
}

KH_LaunchGhostty(shellKind, launchDir) {
    global KH_GHOSTTY_CONFIG_BY_SHELL, KH_GHOSTTY_CONFIG_PATH

    configPath := KH_GHOSTTY_CONFIG_BY_SHELL.Has(shellKind)
        ? KH_GHOSTTY_CONFIG_BY_SHELL[shellKind]
        : KH_GHOSTTY_CONFIG_PATH
    shellArgs := KH_GetShellArgs(shellKind)

    if shellKind = "ps5" {
        command := KH_JoinCommand([
            "ghostty",
            "--working-directory=" launchDir,
            "--config-file=" configPath,
            "--command=" KH_JoinCommand(shellArgs)
        ])
    } else {
        command := KH_JoinCommand([
            "ghostty",
            "--working-directory=" launchDir,
            "--config-file=" configPath,
            "-e"
        ]) " " KH_JoinCommand(shellArgs)
    }

    Run(command, launchDir)
}

KH_GetShellArgs(shellKind) {
    global KH_PS5_PROFILE_PATH

    if shellKind = "ps5" {
        if FileExist(KH_PS5_PROFILE_PATH) {
            return [
                "powershell",
                "-NoLogo",
                "-NoExit",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                ". " KH_QuotePowerShellSingle(KH_PS5_PROFILE_PATH)
            ]
        }
        return ["powershell", "-NoLogo"]
    }

    return ["pwsh", "-NoLogo"]
}

KH_QuotePowerShellSingle(value) {
    return "'" StrReplace(value, "'", "''") "'"
}

KH_JoinCommand(args) {
    command := ""
    for arg in args {
        if command != "" {
            command .= " "
        }
        command .= KH_QuoteCommandArg(arg)
    }
    return command
}

KH_QuoteCommandArg(arg) {
    arg := String(arg)
    if arg = "" {
        return '""'
    }
    if !RegExMatch(arg, '[\s"]') {
        return arg
    }
    return '"' StrReplace(arg, '"', '\"') '"'
}
