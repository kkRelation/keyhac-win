global KH_U0IsDown := false
global KH_U0LastUpTick := 0
global KH_U0LWinPendingTap := false
global KH_SendingNativeLWin := false

KH_InitNativePassthroughExt() {
    Hotkey "~*F19", KH_OnU0Down
    Hotkey "~*F19 Up", KH_OnU0Up
    Hotkey "~*LWin", KH_OnLWinDown
    Hotkey "~*LWin Up", KH_OnLWinUp
}

KH_OnU0Down(*) {
    global KH_U0IsDown
    KH_U0IsDown := true
}

KH_OnU0Up(*) {
    global KH_U0IsDown, KH_U0LastUpTick
    KH_U0IsDown := false
    KH_U0LastUpTick := A_TickCount
}

KH_OnLWinDown(*) {
    global KH_U0LWinPendingTap, KH_SendingNativeLWin

    if KH_SendingNativeLWin {
        return
    }

    KH_U0LWinPendingTap := KH_IsU0ActiveForNativeTap()
}

KH_OnLWinUp(*) {
    global KH_U0LWinPendingTap, KH_SendingNativeLWin

    if KH_SendingNativeLWin {
        return
    }

    shouldTap := KH_U0LWinPendingTap && A_PriorKey = "LWin"
    KH_U0LWinPendingTap := false
    if !shouldTap {
        return
    }

    KH_SendingNativeLWin := true
    try {
        SendEvent "{LWin Down}{LWin Up}"
    } finally {
        KH_SendingNativeLWin := false
    }
}

KH_IsU0ActiveForNativeTap() {
    global KH_U0IsDown, KH_U0LastUpTick
    return KH_U0IsDown || (A_TickCount - KH_U0LastUpTick <= 120)
}
