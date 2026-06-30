KH_InitMoveWindowExt() {
    KH_Bind("U0-J", (*) => KH_MoveActiveWindow(-10, 0))
    KH_Bind("U0-K", (*) => KH_MoveActiveWindow(0, 10))
    KH_Bind("U0-L", (*) => KH_MoveActiveWindow(10, 0))
    KH_Bind("U0-I", (*) => KH_MoveActiveWindow(0, -10))

    KH_Bind("C-U0-J", (*) => KH_MoveActiveWindow(-50, 0))
    KH_Bind("C-U0-K", (*) => KH_MoveActiveWindow(0, 50))
    KH_Bind("C-U0-L", (*) => KH_MoveActiveWindow(50, 0))
    KH_Bind("C-U0-I", (*) => KH_MoveActiveWindow(0, -50))

    KH_Bind("C-S-U0-J", (*) => KH_MoveActiveWindow(-200, 0))
    KH_Bind("C-S-U0-K", (*) => KH_MoveActiveWindow(0, 200))
    KH_Bind("C-S-U0-L", (*) => KH_MoveActiveWindow(200, 0))
    KH_Bind("C-S-U0-I", (*) => KH_MoveActiveWindow(0, -200))
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
