import ctypes
from ctypes import wintypes


_user32 = ctypes.windll.user32

INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("u", INPUT_UNION)]


_VK_MAP = {
    "OPENBRACKET": 0xDB,
    "CLOSEBRACKET": 0xDD,
    "LEFT": 0x25,
    "RIGHT": 0x27,
    "UP": 0x26,
    "DOWN": 0x28,
    "SPACE": 0x20,
    "ENTER": 0x0D,
    "BACK": 0x08,
    "TAB": 0x09,
}


def _make_keyboard_input(vk, up=False):
    key_input = KEYBDINPUT()
    key_input.wVk = vk
    key_input.wScan = _user32.MapVirtualKeyW(vk, 0)
    key_input.dwFlags = KEYEVENTF_SCANCODE
    if up:
        key_input.dwFlags |= KEYEVENTF_KEYUP
    if vk in (0x25, 0x26, 0x27, 0x28, 0x12, 0x11, 0x5B, 0x5C, 0x2D, 0x2E, 0x24, 0x23, 0x21, 0x22, 0x0D):
        key_input.dwFlags |= KEYEVENTF_EXTENDEDKEY

    event = INPUT()
    event.type = INPUT_KEYBOARD
    event.u.ki = key_input
    return event


def direct_inject_keys(keys_str):
    parts = keys_str.split("-")
    modifiers = []
    vk = None
    for index, part in enumerate(parts):
        part = part.upper()
        if index < len(parts) - 1:
            if part == "C":
                modifiers.append(0x11)
            elif part == "A":
                modifiers.append(0x12)
            elif part == "S":
                modifiers.append(0x10)
            elif part == "W":
                modifiers.append(0x5B)
        else:
            if len(part) == 1:
                vk = ord(part)
            elif part in _VK_MAP:
                vk = _VK_MAP[part]

    if vk is None:
        return

    inputs = []
    for modifier in modifiers:
        inputs.append(_make_keyboard_input(modifier, False))

    inputs.append(_make_keyboard_input(vk, False))
    inputs.append(_make_keyboard_input(vk, True))

    for modifier in reversed(modifiers):
        inputs.append(_make_keyboard_input(modifier, True))

    if inputs:
        lp_input = (INPUT * len(inputs))(*inputs)
        _user32.SendInput(len(inputs), lp_input, ctypes.sizeof(INPUT))
