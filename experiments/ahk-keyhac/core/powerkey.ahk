#Requires AutoHotkey v2.0

global KH_PowerKeyScopes := Map()
global KH_PowerKeyScopeOrder := []
global KH_PowerKeyRegisteredPrefixes := Map()
global KH_PowerKeyRegisteredActiveKeys := Map()
global KH_PowerKeyActiveCtx := ""
global KH_PowerKeyTapTimeoutMs := 50

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
    __New(prefix, keyName, nodes) {
        this.prefix := prefix
        this.keyName := keyName
        this.nodes := nodes
        this.matched := []
        this.down := true
        this.done := false
        this.gen := 0
    }
}

KH_PowerKey_Add(prefix, sequence, action, scopeName := "__global__", winTitle := "") {
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
        KH_PowerKey_RegisterActiveKey(key)
    }
    node.action := action

    KH_PowerKey_RegisterPrefix(prefix)
    KH_PowerKey_RegisterFlushers()
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

KH_PowerKey_RegisterPrefix(key) {
    global KH_PowerKeyRegisteredPrefixes

    if KH_PowerKeyRegisteredPrefixes.Has(key) {
        return
    }

    keyName := KH_PowerKey_KeyToHotkey(key)
    HotIf
    Hotkey "$" keyName, (*) => KH_PowerKey_OnKeyDown(key)
    Hotkey "$" keyName " up", (*) => KH_PowerKey_OnKeyUp(key)
    KH_PowerKeyRegisteredPrefixes[key] := true
}

KH_PowerKey_RegisterActiveKey(key) {
    global KH_PowerKeyRegisteredActiveKeys

    if KH_PowerKeyRegisteredActiveKeys.Has(key) {
        return
    }

    keyName := KH_PowerKey_KeyToHotkey(key)
    HotIf KH_PowerKey_IsActive
    Hotkey "$" keyName, (*) => KH_PowerKey_OnKeyDown(key)
    Hotkey "$" keyName " up", (*) => KH_PowerKey_OnKeyUp(key)
    HotIf
    KH_PowerKeyRegisteredActiveKeys[key] := true
}

KH_PowerKey_RegisterFlushers() {
    for key in KH_PowerKey_FlusherKeys() {
        KH_PowerKey_RegisterActiveKey(key)
    }
}

KH_PowerKey_FlusherKeys() {
    keys := []
    Loop 26 {
        keys.Push(Chr(96 + A_Index))
    }
    Loop 10 {
        keys.Push(String(A_Index - 1))
    }
    for key in [
        "-", "=", ",", ".", ";", "/", "\", "[", "]", "'", "``",
        "space", "tab", "back", "enter", "esc",
        "insert", "delete", "home", "end", "pageup", "pagedown",
        "left", "right", "up", "down",
        "appskey", "printscreen", "scrolllock", "pause", "numlock",
        "divide", "multiply", "subtract", "add", "decimal"
    ] {
        keys.Push(key)
    }
    Loop 12 {
        keys.Push("f" A_Index)
    }
    Loop 10 {
        keys.Push("numpad" (A_Index - 1))
    }
    keys.Push("lwin")
    keys.Push("rwin")
    return keys
}

KH_PowerKey_IsActive(*) {
    global KH_PowerKeyActiveCtx
    return KH_PowerKeyActiveCtx != ""
}

KH_PowerKey_OnKeyDown(key) {
    global KH_PowerKeyActiveCtx

    ctx := KH_PowerKeyActiveCtx
    if ctx != "" {
        if key = ctx.prefix {
            ctx.gen += 1
            if ctx.down {
                ctx.done := true
                KH_PowerKey_SendKey(key)
                return
            }
            KH_PowerKey_SendKey(key)
            KH_PowerKeyActiveCtx := ""
        } else if KH_PowerKey_TrySuffixDown(ctx, key) {
            return
        }
    }

    nodes := KH_PowerKey_ActiveRoots(key)
    if nodes.Length = 0 {
        KH_PowerKey_SendKey(key)
        return
    }

    KH_PowerKeyActiveCtx := KH_PowerKeyContext(key, KH_PowerKey_KeyToHotkey(key), nodes)
}

KH_PowerKey_OnKeyUp(key) {
    global KH_PowerKeyActiveCtx

    ctx := KH_PowerKeyActiveCtx
    if ctx = "" {
        return
    }

    if key = ctx.prefix {
        ctx.down := false
        if ctx.done {
            KH_PowerKeyActiveCtx := ""
            return
        }
        if ctx.matched.Length = 0 {
            KH_PowerKey_ScheduleTap(ctx)
            return
        }
        if KH_PowerKey_HasNext(ctx) {
            KH_PowerKey_ScheduleCancel(ctx)
            return
        }
        KH_PowerKey_Cancel(ctx, true)
        return
    }

    KH_PowerKey_TrySuffixUp(ctx, key)
}

KH_PowerKey_TrySuffixDown(ctx, key) {
    global KH_PowerKeyActiveCtx

    ctx.gen += 1
    nextNodes := []
    for node in ctx.nodes {
        if node.children.Has(key) {
            nextNodes.Push(node.children[key])
        }
    }

    if nextNodes.Length = 0 {
        KH_PowerKey_Cancel(ctx, true)
        return false
    }

    ctx.nodes := nextNodes
    ctx.matched.Push(key)
    for node in nextNodes {
        if node.action != "" {
            node.action.Call()
            ctx.done := true
            KH_PowerKeyActiveCtx := ""
            return true
        }
    }
    return true
}

KH_PowerKey_TrySuffixUp(ctx, key) {
    if ctx.matched.Length = 0 || key != ctx.matched[ctx.matched.Length] {
        return false
    }

    if !ctx.down && KH_PowerKey_HasNext(ctx) {
        KH_PowerKey_Cancel(ctx, true)
        return true
    }
    return true
}

KH_PowerKey_HasNext(ctx) {
    for node in ctx.nodes {
        if node.children.Count > 0 {
            return true
        }
    }
    return false
}

KH_PowerKey_ScheduleTap(ctx) {
    global KH_PowerKeyTapTimeoutMs

    ctx.gen += 1
    gen := ctx.gen
    SetTimer((*) => KH_PowerKey_TapExpired(ctx, gen), -KH_PowerKeyTapTimeoutMs)
}

KH_PowerKey_TapExpired(ctx, gen) {
    global KH_PowerKeyActiveCtx

    if KH_PowerKeyActiveCtx == ctx && ctx.gen = gen && !ctx.done {
        KH_PowerKey_SendKey(ctx.prefix)
        KH_PowerKeyActiveCtx := ""
    }
}

KH_PowerKey_ScheduleCancel(ctx) {
    global KH_PowerKeyTapTimeoutMs

    ctx.gen += 1
    gen := ctx.gen
    SetTimer((*) => KH_PowerKey_CancelExpired(ctx, gen), -KH_PowerKeyTapTimeoutMs)
}

KH_PowerKey_CancelExpired(ctx, gen) {
    global KH_PowerKeyActiveCtx

    if KH_PowerKeyActiveCtx == ctx && ctx.gen = gen && !ctx.done {
        KH_PowerKey_Cancel(ctx, true)
    }
}

KH_PowerKey_Cancel(ctx, emitPrefix) {
    global KH_PowerKeyActiveCtx

    KH_PowerKeyActiveCtx := ""
    if emitPrefix {
        KH_PowerKey_SendKey(ctx.prefix)
        Sleep(10)
    }
    for key in ctx.matched {
        KH_PowerKey_SendKey(key)
        Sleep(10)
    }
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
        "plus", "=",
        "pgup", "pageup",
        "pgdn", "pagedown",
        "apps", "appskey",
        "numpad0", "numpad0",
        "num0", "numpad0",
        "num1", "numpad1",
        "num2", "numpad2",
        "num3", "numpad3",
        "num4", "numpad4",
        "num5", "numpad5",
        "num6", "numpad6",
        "num7", "numpad7",
        "num8", "numpad8",
        "num9", "numpad9"
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
        "'", "'",
        "``", "``",
        "-", "-",
        "=", "=",
        "space", "Space",
        "tab", "Tab",
        "enter", "Enter",
        "esc", "Escape",
        "back", "Backspace",
        "insert", "Insert",
        "delete", "Delete",
        "home", "Home",
        "end", "End",
        "pageup", "PgUp",
        "pagedown", "PgDn",
        "left", "Left",
        "right", "Right",
        "up", "Up",
        "down", "Down",
        "appskey", "AppsKey",
        "printscreen", "PrintScreen",
        "scrolllock", "ScrollLock",
        "pause", "Pause",
        "numlock", "NumLock",
        "divide", "NumpadDiv",
        "multiply", "NumpadMult",
        "subtract", "NumpadSub",
        "add", "NumpadAdd",
        "decimal", "NumpadDot",
        "lwin", "LWin",
        "rwin", "RWin"
    )
    if RegExMatch(key, "^f\d+$") {
        return StrUpper(key)
    }
    if RegExMatch(key, "^numpad\d$") {
        return "Numpad" SubStr(key, 7)
    }
    return aliases.Has(key) ? aliases[key] : key
}

KH_PowerKey_SendKey(key) {
    sendName := KH_PowerKey_KeyToHotkey(key)
    SendEvent "{Blind}{" sendName "}"
}
