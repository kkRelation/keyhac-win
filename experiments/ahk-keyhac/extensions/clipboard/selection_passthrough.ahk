global KH_SelectionProbeRunning := false

KH_InitSelectionPassthroughExt() {
    KH_Bind("U0-A", (*) => KH_CopySelectionBeforeAltL())
}

KH_CopySelectionBeforeAltL() {
    KH_CopySelectionBeforePassthrough(() => SendEvent("!l"))
}

KH_CopySelectionBeforePassthrough(sendPassthrough, copyKeys := "^c", timeoutMs := 300, pollMs := 15) {
    global KH_SelectionProbeRunning

    if KH_SelectionProbeRunning {
        return
    }
    KH_SelectionProbeRunning := true

    sentinel := Chr(0) "__KH_SENTINEL__" Chr(0)
    previousClipboard := ClipboardAll()
    A_Clipboard := sentinel

    startTick := A_TickCount

    doCopy := (*) => SendEvent(copyKeys)
    pollClipboard := ""
    pollClipboard := (*) => (
        KH_CheckSelectionProbe(
            sentinel,
            previousClipboard,
            sendPassthrough,
            startTick,
            timeoutMs,
            pollMs,
            pollClipboard
        )
    )

    SetTimer(doCopy, -30)
    SetTimer(pollClipboard, -45)
}

KH_CheckSelectionProbe(sentinel, previousClipboard, sendPassthrough, startTick, timeoutMs, pollMs, pollClipboard) {
    global KH_SelectionProbeRunning

    clipboardText := A_Clipboard
    if clipboardText != "" && clipboardText != sentinel {
        KH_SelectionProbeRunning := false
        SetTimer((*) => sendPassthrough.Call(), -50)
        return
    }

    if A_TickCount - startTick >= timeoutMs {
        A_Clipboard := previousClipboard
        KH_SelectionProbeRunning := false
        SetTimer((*) => sendPassthrough.Call(), -50)
        return
    }

    SetTimer(pollClipboard, -pollMs)
}
