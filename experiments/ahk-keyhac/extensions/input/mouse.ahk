KH_InitMouseExt() {
    KH_Bind("U0-Left", (*) => MouseMove(-10, 0, 0, "R"))
    KH_Bind("U0-Right", (*) => MouseMove(10, 0, 0, "R"))
    KH_Bind("U0-Up", (*) => MouseMove(0, -10, 0, "R"))
    KH_Bind("U0-Down", (*) => MouseMove(0, 10, 0, "R"))

    KH_Bind("D-U0-Space", (*) => Click("Left Down"))
    KH_Bind("U-U0-Space", (*) => Click("Left Up"))

    KH_Bind("U0-PageUp", (*) => Click("WheelUp"))
    KH_Bind("U0-PageDown", (*) => Click("WheelDown"))
    KH_Bind("U0-Home", (*) => Click("WheelLeft"))
    KH_Bind("U0-End", (*) => Click("WheelRight"))

    KH_Bind("C-U0-PageUp", (*) => MouseClick("WheelUp", , , 5))
    KH_Bind("C-U0-PageDown", (*) => MouseClick("WheelDown", , , 5))
    KH_Bind("C-U0-Home", (*) => MouseClick("WheelLeft", , , 5))
    KH_Bind("C-U0-End", (*) => MouseClick("WheelRight", , , 5))

    KH_Bind("C-S-U0-PageUp", (*) => MouseClick("WheelUp", , , 20))
    KH_Bind("C-S-U0-PageDown", (*) => MouseClick("WheelDown", , , 20))
    KH_Bind("C-S-U0-Home", (*) => MouseClick("WheelLeft", , , 20))
    KH_Bind("C-S-U0-End", (*) => MouseClick("WheelRight", , , 20))
}
