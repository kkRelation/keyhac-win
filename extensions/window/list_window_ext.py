import ctypes

from keyhac import *

_search_active = False
_DEBUG = True


class _GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("hwndActive", ctypes.c_void_p),
        ("hwndFocus", ctypes.c_void_p),
        ("hwndCapture", ctypes.c_void_p),
        ("hwndMenuOwner", ctypes.c_void_p),
        ("hwndMoveSize", ctypes.c_void_p),
        ("hwndCaret", ctypes.c_void_p),
        ("rcCaret", ctypes.c_long * 4),
    ]


def _window_class_name(hwnd):
    if not hwnd:
        return None
    try:
        buffer = ctypes.create_unicode_buffer(256)
        if not ctypes.windll.user32.GetClassNameW(hwnd, buffer, len(buffer)):
            return None
        return buffer.value
    except Exception:
        return None


def _window_text(hwnd):
    if not hwnd:
        return None
    try:
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buffer = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buffer, len(buffer))
        return buffer.value
    except Exception:
        return None


def _gui_thread_info():
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return None

    thread_id = user32.GetWindowThreadProcessId(hwnd, None)
    info = _GUITHREADINFO()
    info.cbSize = ctypes.sizeof(info)
    if not user32.GetGUIThreadInfo(thread_id, ctypes.byref(info)):
        return None
    return hwnd, thread_id, info


def _focused_class_name():
    try:
        snapshot = _gui_thread_info()
        if snapshot is None:
            return None
        _, _, info = snapshot
        if not info.hwndFocus:
            return None
        return _window_class_name(info.hwndFocus)
    except Exception:
        return None


def _is_search_active():
    class_name = _focused_class_name()
    if class_name is not None:
        return "edit" in class_name.lower()
    return _search_active


def _debug_print_state(keymap, label):
    if not _DEBUG:
        return
    try:
        snapshot = _gui_thread_info()
        if snapshot is None:
            print(f"[list_window_ext] {label}: no gui thread info")
            return

        hwnd, thread_id, info = snapshot
        print(
            "[list_window_ext] "
            f"{label}: "
            f"is_list={keymap.isListWindowOpened()} "
            f"tracked_search={_search_active} "
            f"detected_search={_is_search_active()} "
            f"thread={thread_id} "
            f"active_class={_window_class_name(hwnd)!r} "
            f"active_text={_window_text(hwnd)!r} "
            f"focus_class={_window_class_name(info.hwndFocus)!r} "
            f"focus_text={_window_text(info.hwndFocus)!r} "
            f"caret_class={_window_class_name(info.hwndCaret)!r} "
            f"caret_text={_window_text(info.hwndCaret)!r}"
        )
    except Exception as exc:
        print(f"[list_window_ext] {label}: debug failed: {exc!r}")


def schedule_list_window_search(keymap, delay_ms=100):
    def start_search():
        global _search_active
        if keymap.isListWindowOpened():
            keymap.InputKeyCommand("F")()
            _search_active = True

    keymap.delayedCall(start_search, delay_ms)


def _switch_list_and_resume_search(keymap, direction):
    def _command():
        global _search_active
        if not keymap.isListWindowOpened():
            return
        _search_active = False
        keymap.InputKeyCommand("Esc")()

        def _continue_switch():
            global _search_active
            if not keymap.isListWindowOpened():
                return
            keymap.InputKeyCommand(direction)()
            schedule_list_window_search(keymap, delay_ms=35)

        keymap.delayedCall(_continue_switch, 30)

    return _command


def _move_list_selection(keymap, direction):
    def _command():
        if not keymap.isListWindowOpened():
            return
        keymap.InputKeyCommand(direction)()

    return _command


def _escape_list_window(keymap):
    def _command():
        global _search_active
        if keymap.isListWindowOpened():
            _search_active = False
        keymap.InputKeyCommand("Esc")()

    return _command


def _debug_list_window_state(keymap):
    def _command():
        _debug_print_state(keymap, "manual")

    return _command


def init_list_window_ext(keymap):
    # Match the whole keyhac.exe process instead of child control classes,
    # because incremental search moves focus between internal controls.
    keymap_listwindow = keymap.defineWindowKeymap(exe_name="keyhac.exe")
    keymap_listwindow["C-J"] = _move_list_selection(keymap, "Down")
    keymap_listwindow["C-K"] = _move_list_selection(keymap, "Up")
    keymap_listwindow["C-H"] = _switch_list_and_resume_search(keymap, "Left")
    keymap_listwindow["C-L"] = _switch_list_and_resume_search(keymap, "Right")
    keymap_listwindow["Esc"] = _escape_list_window(keymap)
    keymap_listwindow["C-S-D"] = _debug_list_window_state(keymap)
