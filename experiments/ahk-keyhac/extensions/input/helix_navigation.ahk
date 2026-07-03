#Requires AutoHotkey v2.0

KH_InitHelixNavigationExt() {
    KH_Bind("H1-H", (*) => SendEvent("{Blind}{Left}"))
    KH_Bind("H1-J", (*) => SendEvent("{Blind}{Down}"))
    KH_Bind("H1-K", (*) => SendEvent("{Blind}{Up}"))
    KH_Bind("H1-L", (*) => SendEvent("{Blind}{Right}"))

    KH_Bind("H1-Y", (*) => SendEvent("{Blind}^{Left}"))
    KH_Bind("H1-O", (*) => SendEvent("{Blind}^{Right}"))
    KH_Bind("H1-N", (*) => SendEvent("{Blind}{Home}"))
    KH_Bind("H1-M", (*) => SendEvent("{Blind}{End}"))
    KH_Bind("H1-U", (*) => SendEvent("{Blind}{PgUp}"))
    KH_Bind("H1-I", (*) => SendEvent("{Blind}{PgDn}"))

    KH_Bind("A-H1-H", (*) => Click("WheelLeft"))
    KH_Bind("A-H1-J", (*) => Click("WheelDown"))
    KH_Bind("A-H1-K", (*) => Click("WheelUp"))
    KH_Bind("A-H1-L", (*) => Click("WheelRight"))

    KH_Bind("C-A-H1-H", (*) => MouseClick("WheelLeft", , , 5))
    KH_Bind("C-A-H1-J", (*) => MouseClick("WheelDown", , , 5))
    KH_Bind("C-A-H1-K", (*) => MouseClick("WheelUp", , , 5))
    KH_Bind("C-A-H1-L", (*) => MouseClick("WheelRight", , , 5))
}
