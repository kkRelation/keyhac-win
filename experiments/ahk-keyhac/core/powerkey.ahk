#Requires AutoHotkey v2.0

global KH_PowerKeyScopes := Map()
global KH_PowerKeyScopeOrder := []
global KH_PowerKeyRegisteredPrefixes := Map()
global KH_PowerKeyActiveCtx := ""
global KH_PowerKeyTimeoutSeconds := 0.45

class KH_PowerKeyNode {
    __New() {
        this.children := Map()
        this.action := ""
    }
}

class KH_PowerKeyScope {
    __New(name, winTitle := "") {
        this.name := name
        this.winTitle := winTitle
        this.roots := Map()
    }
}

class KH_PowerKeyContext {
    __New(prefix, nodes) {
        this.prefix := prefix
        this.nodes := nodes
        this.matched := []
        this.hook := ""
    }
}

KH_PowerKey_Add(prefix, sequence, action, scopeName := "__global__", winTitle := "") {
    global KH_PowerKeyRegisteredPrefixes

    prefix := KH_PowerKey_CanonicalKey(prefix)
    keys := KH_PowerKey_ParseSequence(sequence)
    if keys.Length = 0 {
        throw ValueError("PowerKey sequence must contain at least one suffix key.", -1, sequence)
    }

    scope := KH_PowerKey_GetScope(scopeName, winTitle)
    if !scope.roots.Has(prefix) {
        scope.roots[prefix] := KH_PowerKeyNode()
    }

    node := scope.roots[prefix]
    for key in keys {
        key := KH_PowerKey_CanonicalKey(key)
        if !node.children.Has(key) {
            node.children[key] := KH_PowerKeyNode()
        }
        node := node.children[key]
    }
    node.action := action

    if !KH_PowerKeyRegisteredPrefixes.Has(prefix) {
        hotkeyName := "$" KH_PowerKey_KeyToHotkey(prefix)
        Hotkey hotkeyName, (*) => KH_PowerKey_Start(prefix)
        KH_PowerKeyRegisteredPrefixes[prefix] := true
    }
}

KH_PowerKey_AddMany(prefix, sequenceMap, scopeName := "__global__", winTitle := "") {
    for sequence, action in sequenceMap {
        KH_PowerKey_Add(prefix, sequence, action, scopeName, winTitle)
    }
}

KH_PowerKey_GetScope(scopeName, winTitle := "") {
    global KH_PowerKeyScopes, KH_PowerKeyScopeOrder

    if !KH_PowerKeyScopes.Has(scopeName) {
        scope := KH_PowerKeyScope(scopeName, winTitle)
        KH_PowerKeyScopes[scopeName] := scope
        KH_PowerKeyScopeOrder.Push(scopeName)
    } else {
        scope := KH_PowerKeyScopes[scopeName]
        if winTitle != "" {
            scope.winTitle := winTitle
        }
    }
    return scope
}

KH_PowerKey_ParseSequence(sequence) {
    if Type(sequence) = "Array" {
        return sequence
    }

    parts := []
    for part in StrSplit(String(sequence), "-") {
        if part != "" {
            parts.Push(part)
        }
    }
    return parts
}

KH_PowerKey_Start(prefix) {
    global KH_PowerKeyActiveCtx

    nodes := KH_PowerKey_ActiveRoots(prefix)
    if nodes.Length = 0 {
        KH_PowerKey_SendKey(prefix)
        return
    }

    ctx := KH_PowerKeyContext(prefix, nodes)
    KH_PowerKeyActiveCtx := ctx
    KH_PowerKey_StartInput(ctx)
}

KH_PowerKey_ActiveRoots(prefix) {
    global KH_PowerKeyScopes, KH_PowerKeyScopeOrder

    nodes := []
    index := KH_PowerKeyScopeOrder.Length
    while index >= 1 {
        scope := KH_PowerKeyScopes[KH_PowerKeyScopeOrder[index]]
        index -= 1

        if scope.winTitle != "" && !WinActive(scope.winTitle) {
            continue
        }
        if scope.roots.Has(prefix) {
            nodes.Push(scope.roots[prefix])
        }
    }
    return nodes
}

KH_PowerKey_StartInput(ctx) {
    global KH_PowerKeyTimeoutSeconds

    ih := InputHook("L0 T" KH_PowerKeyTimeoutSeconds)
    ih.VisibleNonText := false
    ih.KeyOpt("{All}", "E")
    ih.KeyOpt("{LCtrl}{RCtrl}{LAlt}{RAlt}{LShift}{RShift}{LWin}{RWin}", "-E")
    ih.OnEnd := (hook) => KH_PowerKey_OnInputEnd(ctx, hook)
    ctx.hook := ih
    ih.Start()
}

KH_PowerKey_OnInputEnd(ctx, hook) {
    global KH_PowerKeyActiveCtx

    if KH_PowerKeyActiveCtx != ctx {
        return
    }

    if hook.EndReason != "EndKey" {
        KH_PowerKey_Cancel(ctx)
        return
    }

    key := KH_PowerKey_CanonicalKey(hook.EndKey)
    nextNodes := []
    for node in ctx.nodes {
        if node.children.Has(key) {
            nextNodes.Push(node.children[key])
        }
    }

    ctx.matched.Push(key)
    if nextNodes.Length = 0 {
        KH_PowerKey_Cancel(ctx)
        return
    }

    ctx.nodes := nextNodes
    for node in nextNodes {
        if node.action != "" {
            KH_PowerKeyActiveCtx := ""
            node.action.Call()
            return
        }
    }

    KH_PowerKey_StartInput(ctx)
}

KH_PowerKey_Cancel(ctx) {
    global KH_PowerKeyActiveCtx

    KH_PowerKeyActiveCtx := ""
    KH_PowerKey_SendKey(ctx.prefix)
    for key in ctx.matched {
        KH_PowerKey_SendKey(key)
    }
}

KH_PowerKey_CanonicalKey(key) {
    key := StrLower(String(key))
    aliases := Map(
        "escape", "esc",
        "return", "enter",
        "semicolon", ";",
        "comma", ",",
        "period", ".",
        "slash", "/",
        "backslash", "\",
        "openbracket", "[",
        "closebracket", "]",
        "minus", "-",
        "equal", "=",
        "pgup", "pageup",
        "pgdn", "pagedown"
    )
    return aliases.Has(key) ? aliases[key] : key
}

KH_PowerKey_KeyToHotkey(key) {
    aliases := Map(
        ";", ";",
        ",", ",",
        ".", ".",
        "/", "/",
        "\", "\",
        "[", "[",
        "]", "]",
        "-", "-",
        "=", "=",
        "space", "Space",
        "tab", "Tab",
        "enter", "Enter",
        "esc", "Escape",
        "back", "Backspace",
        "pageup", "PgUp",
        "pagedown", "PgDn"
    )
    return aliases.Has(key) ? aliases[key] : key
}

KH_PowerKey_SendKey(key) {
    sendName := KH_PowerKey_KeyToHotkey(key)
    if StrLen(key) = 1 {
        SendText key
    } else {
        SendEvent "{" sendName "}"
    }
}
