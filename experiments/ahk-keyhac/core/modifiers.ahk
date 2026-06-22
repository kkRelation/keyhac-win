#Requires AutoHotkey v2.0

global KH_UserModifierKeys := Map(
    "U0", "F19",
    "U1", "F20",
    "U2", "F21",
    "U3", "F22",
    "U4", "F23"
)

global KH_ModifierSymbols := Map(
    "A", "!",
    "C", "^",
    "S", "+",
    "W", "#",
    "LA", "<!",
    "LC", "<^",
    "LS", "<+",
    "LW", "<#",
    "RA", ">!",
    "RC", ">^",
    "RS", ">+",
    "RW", ">#"
)

global KH_KanataChordAliases := Map(
    ; kanata_config/win_to_f19.kbd maps real caps+spc to this chord.
    "U1-SPACE", "^!+F12"
)

KH_InitUserModifiers() {
    ; Keep physical key state reliable for F19-F23 and future diagnostics.
    InstallKeybdHook true
}

KH_Bind(chord, action, options := "On") {
    spec := KH_ParseChord(chord)
    condition := KH_MakeCondition(spec.userMods)

    HotIf condition
    try {
        Hotkey spec.hotkey, action, options
    } finally {
        HotIf
    }
}

KH_ParseChord(chord) {
    global KH_UserModifierKeys, KH_ModifierSymbols, KH_KanataChordAliases

    parts := StrSplit(chord, "-")
    if parts.Length < 2 {
        throw ValueError("Chord must contain at least one modifier and one key.", -1, chord)
    }

    userMods := []
    semanticMods := []
    nativePrefix := ""
    edge := ""

    Loop parts.Length - 1 {
        token := StrUpper(parts[A_Index])
        if KH_UserModifierKeys.Has(token) {
            userMods.Push(token)
            semanticMods.Push(token)
        } else if KH_ModifierSymbols.Has(token) {
            nativePrefix .= KH_ModifierSymbols[token]
            semanticMods.Push(token)
        } else if token = "D" || token = "U" {
            if edge != "" {
                throw ValueError("Only one edge token is allowed.", -1, chord)
            }
            edge := token
        } else {
            throw ValueError("Unknown modifier token.", -1, token)
        }
    }

    suffix := parts[parts.Length]
    canonicalChord := KH_CanonicalChord(semanticMods, suffix)
    if KH_KanataChordAliases.Has(canonicalChord) {
        hotkeyName := "*" KH_KanataChordAliases[canonicalChord]
    } else {
        hotkeyName := "*" nativePrefix KH_NormalizeKeyName(suffix)
    }

    if edge = "U" {
        hotkeyName .= " Up"
    }

    return { chord: chord, userMods: userMods, hotkey: hotkeyName }
}

KH_CanonicalChord(mods, suffix) {
    canonical := ""
    for modName in mods {
        canonical .= (canonical = "" ? "" : "-") modName
    }
    return canonical "-" StrUpper(suffix)
}

KH_MakeCondition(userMods) {
    global KH_UserModifierKeys
    physicalKeys := []
    for modName in userMods {
        physicalKeys.Push(KH_UserModifierKeys[modName])
    }
    return (*) => KH_AllKeysDown(physicalKeys)
}

KH_AllKeysDown(keys) {
    for keyName in keys {
        if !GetKeyState(keyName, "P") {
            return false
        }
    }
    return true
}

KH_NormalizeKeyName(keyName) {
    aliases := Map(
        "ESC", "Escape",
        "SEMICOLON", ";",
        "COMMA", ",",
        "PERIOD", ".",
        "SLASH", "/",
        "BACKSLASH", "\",
        "OPENBRACKET", "[",
        "CLOSEBRACKET", "]",
        "MINUS", "-",
        "EQUAL", "="
    )

    upper := StrUpper(keyName)
    if aliases.Has(upper) {
        return aliases[upper]
    }
    return keyName
}
