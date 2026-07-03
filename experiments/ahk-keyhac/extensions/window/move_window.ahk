KH_InitMoveWindowExt() {
    KH_Bind("U0-Home", (*) => KH_MoveActiveWindow(-10, 0))
    KH_Bind("U0-PageDown", (*) => KH_MoveActiveWindow(0, 10))
    KH_Bind("U0-PageUp", (*) => KH_MoveActiveWindow(0, -10))
    KH_Bind("U0-End", (*) => KH_MoveActiveWindow(10, 0))

    KH_Bind("S-U0-Home", (*) => KH_MoveActiveWindow(-1, 0))
    KH_Bind("S-U0-PageDown", (*) => KH_MoveActiveWindow(0, 1))
    KH_Bind("S-U0-PageUp", (*) => KH_MoveActiveWindow(0, -1))
    KH_Bind("S-U0-End", (*) => KH_MoveActiveWindow(1, 0))

    KH_Bind("C-U0-Home", (*) => KH_MoveActiveWindow(-50, 0))
    KH_Bind("C-U0-PageDown", (*) => KH_MoveActiveWindow(0, 50))
    KH_Bind("C-U0-PageUp", (*) => KH_MoveActiveWindow(0, -50))
    KH_Bind("C-U0-End", (*) => KH_MoveActiveWindow(50, 0))

    KH_Bind("C-S-U0-Home", (*) => KH_MoveActiveWindow(-200, 0))
    KH_Bind("C-S-U0-PageDown", (*) => KH_MoveActiveWindow(0, 200))
    KH_Bind("C-S-U0-PageUp", (*) => KH_MoveActiveWindow(0, -200))
    KH_Bind("C-S-U0-End", (*) => KH_MoveActiveWindow(200, 0))
}

KH_MoveActiveWindow(deltaX, deltaY) {
    hwnd := WinExist("A")
    if !hwnd {
        return
    }

    try {
        WinGetPos(&x, &y, &width, &height, "ahk_id " hwnd)
        WinMove(x + deltaX, y + deltaY, width, height, "ahk_id " hwnd)
    }
}
