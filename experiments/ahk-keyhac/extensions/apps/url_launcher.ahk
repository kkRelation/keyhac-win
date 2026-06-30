#Requires AutoHotkey v2.0

KH_InitUrlLauncherExt() {
    KH_PowerKey_Add(
        "y",
        "t-l",
        (*) => KH_OpenUrl("http://localhost:5150/admin.html", "firefox", false, true),
        "__global__",
        "",
        "localhost admin"
    )
}

KH_OpenUrl(url, browser := "", private := false, newWindow := true, extraArgs := "") {
    if browser != "" {
        command := KH_BuildBrowserCommand(url, browser, private, newWindow, extraArgs)
        try {
            Run(command)
            return
        } catch as err {
            try OutputDebug("AHK Keyhac: failed to launch " browser " for " url ": " err.Message)
        }
    }

    Run(url)
}

KH_BuildBrowserCommand(url, browser, private, newWindow, extraArgs := "") {
    executable := KH_ResolveBrowserExecutable(browser)
    browserName := StrLower(executable)
    args := [executable]

    if InStr(browserName, "firefox") {
        if private {
            args.Push("-private-window")
        } else if newWindow {
            args.Push("-new-window")
        }
        args.Push(url)
    } else if InStr(browserName, "chrome") || InStr(browserName, "msedge") || InStr(browserName, "edge") {
        if private {
            args.Push("--incognito")
        }
        if newWindow {
            args.Push("--new-window")
        }
        args.Push(url)
    } else {
        args.Push(url)
    }

    if Type(extraArgs) = "Array" {
        for arg in extraArgs {
            args.Push(arg)
        }
    }

    return KH_UrlLauncherJoinCommand(args)
}

KH_ResolveBrowserExecutable(browser) {
    expanded := KH_ExpandEnvironmentStrings(browser)
    if FileExist(expanded) {
        return expanded
    }

    if !RegExMatch(expanded, "i)\.exe$") {
        exeName := expanded ".exe"
    } else {
        exeName := expanded
    }

    if StrLower(exeName) = "firefox.exe" {
        for base in [EnvGet("ProgramFiles"), EnvGet("ProgramFiles(x86)")] {
            if base = "" {
                continue
            }
            candidate := base "\Mozilla Firefox\firefox.exe"
            if FileExist(candidate) {
                return candidate
            }
        }
    }

    return exeName
}

KH_ExpandEnvironmentStrings(value) {
    requiredSize := DllCall("ExpandEnvironmentStringsW", "Str", value, "Ptr", 0, "UInt", 0, "UInt")
    if requiredSize = 0 {
        return value
    }

    expandedBuffer := Buffer(requiredSize * 2)
    if !DllCall("ExpandEnvironmentStringsW", "Str", value, "Ptr", expandedBuffer, "UInt", requiredSize, "UInt") {
        return value
    }
    return StrGet(expandedBuffer)
}

KH_UrlLauncherJoinCommand(args) {
    command := ""
    for arg in args {
        if command != "" {
            command .= " "
        }
        command .= KH_UrlLauncherQuoteArg(arg)
    }
    return command
}

KH_UrlLauncherQuoteArg(arg) {
    arg := String(arg)
    if arg = "" {
        return '""'
    }
    if !RegExMatch(arg, '[\s"]') {
        return arg
    }
    return '"' StrReplace(arg, '"', '\"') '"'
}
