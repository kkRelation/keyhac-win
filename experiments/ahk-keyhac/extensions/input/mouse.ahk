KH_InitMouseExt() {
    KH_Bind("U0-Left", (*) => MouseMove(-10, 0, 0, "R"))
    KH_Bind("U0-Right", (*) => MouseMove(10, 0, 0, "R"))
    KH_Bind("U0-Up", (*) => MouseMove(0, -10, 0, "R"))
    KH_Bind("U0-Down", (*) => MouseMove(0, 10, 0, "R"))

    KH_Bind("C-U0-Left", (*) => MouseMove(-50, 0, 0, "R"))
    KH_Bind("C-U0-Right", (*) => MouseMove(50, 0, 0, "R"))
    KH_Bind("C-U0-Up", (*) => MouseMove(0, -50, 0, "R"))
    KH_Bind("C-U0-Down", (*) => MouseMove(0, 50, 0, "R"))

    KH_Bind("C-S-U0-Left", (*) => MouseMove(-200, 0, 0, "R"))
    KH_Bind("C-S-U0-Right", (*) => MouseMove(200, 0, 0, "R"))
    KH_Bind("C-S-U0-Up", (*) => MouseMove(0, -200, 0, "R"))
    KH_Bind("C-S-U0-Down", (*) => MouseMove(0, 200, 0, "R"))

    KH_Bind("D-U0-Space", (*) => Click("Left Down"))
    KH_Bind("U-U0-Space", (*) => Click("Left Up"))

    KH_Bind("U0-H", (*) => Click("WheelLeft"))
    KH_Bind("U0-J", (*) => Click("WheelDown"))
    KH_Bind("U0-K", (*) => Click("WheelUp"))
    KH_Bind("U0-L", (*) => Click("WheelRight"))

    KH_Bind("S-U0-H", (*) => Click("WheelLeft"))
    KH_Bind("S-U0-J", (*) => Click("WheelDown"))
    KH_Bind("S-U0-K", (*) => Click("WheelUp"))
    KH_Bind("S-U0-L", (*) => Click("WheelRight"))

    KH_Bind("C-U0-H", (*) => MouseClick("WheelLeft", , , 5))
    KH_Bind("C-U0-J", (*) => MouseClick("WheelDown", , , 5))
    KH_Bind("C-U0-K", (*) => MouseClick("WheelUp", , , 5))
    KH_Bind("C-U0-L", (*) => MouseClick("WheelRight", , , 5))

    KH_Bind("C-S-U0-H", (*) => MouseClick("WheelLeft", , , 20))
    KH_Bind("C-S-U0-J", (*) => MouseClick("WheelDown", , , 20))
    KH_Bind("C-S-U0-K", (*) => MouseClick("WheelUp", , , 20))
    KH_Bind("C-S-U0-L", (*) => MouseClick("WheelRight", , , 20))
}
