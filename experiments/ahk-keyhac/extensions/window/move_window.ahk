KH_InitMoveWindowExt() {
    KH_Bind("C-U0-Left", (*) => KH_MoveActiveWindow(-10, 0))
    KH_Bind("C-U0-Right", (*) => KH_MoveActiveWindow(10, 0))
    KH_Bind("C-U0-Up", (*) => KH_MoveActiveWindow(0, -10))
    KH_Bind("C-U0-Down", (*) => KH_MoveActiveWindow(0, 10))
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
