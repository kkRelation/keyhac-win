#Requires AutoHotkey v2.0

global KH_STATE_CLIENT_EXE := "D:\C2D\Desktop\Code\Python\automation\state_center\target\release\state-client.exe"
global KH_StateCenterWatchPid := 0

KH_InitStateCenter() {
    global KH_STATE_CLIENT_EXE, KH_StateCenterWatchPid

    if !FileExist(KH_STATE_CLIENT_EXE) {
        return
    }

    currentPid := DllCall("GetCurrentProcessId", "UInt")
    command := KH_StateCenterQuoteArg(KH_STATE_CLIENT_EXE)
        . " watch-process --source ahk "
        . currentPid
        . " 3500 1200"

    try {
        Run(command, , "Hide", &KH_StateCenterWatchPid)
    }
}

KH_StateCenterQuoteArg(value) {
    quote := Chr(34)
    return quote StrReplace(String(value), quote, "\" quote) quote
}
