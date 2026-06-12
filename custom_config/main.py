import os
import ctypes
from keyhac import *

def configure(keymap):
    # --------------------------------------------------------------------
    # 基本设置
    keymap.editor = "notepad.exe"
    keymap.setFont("Inconsolata-LXGWMono", 20)
    keymap.setTheme("black")
    keymap.quote_mark = "> "

    # --------------------------------------------------------------------
    # 按键替换与修饰键定义
    keymap.defineModifier(235, "User0")
    keymap.defineModifier(236, "User1")
    keymap.defineModifier(237, "User2")
    # Keyhac only supports User0-User3, so the exposed U3/U4 states are
    # carried by side-specific User3 modifiers internally.
    keymap.defineModifier(238, "LUser3")
    keymap.defineModifier(239, "RUser3")

    # 定义全局键位图
    keymap_global = keymap.defineWindowKeymap()
    from extensions.system.shared_state import read_shared_state, write_shared_state

    # 动态切换 U0-U4 导出模式（User 修饰键 <-> 原生按键）
    shared_state = read_shared_state()
    modifier_specs = [
        {
            "state_key": "win_is_u0",
            "legacy_key": "u0",
            "scan_code": 130,
            "user_code": 235,
            "native_vk": 91,
            "enabled_label": "U0",
            "disabled_label": "WIN",
            "enabled_log": "[Info] Switched Win to User0",
            "disabled_log": "[Info] Switched Win to Native LWin",
        },
        {
            "state_key": "caps_is_u1",
            "legacy_key": "u1",
            "scan_code": 131,
            "user_code": 236,
            "native_vk": 20,
            "enabled_label": "U1",
            "disabled_label": "CAPS",
            "enabled_log": "[Info] Switched CapsLock to User1",
            "disabled_log": "[Info] Switched CapsLock to Native CapsLock",
        },
        {
            "state_key": "ralt_is_u2",
            "legacy_key": "u2",
            "scan_code": 132,
            "user_code": 237,
            "native_vk": 165,
            "enabled_label": "U2",
            "disabled_label": "RAlt",
            "enabled_log": "[Info] Switched RAlt to U2",
            "disabled_log": "[Info] Switched RAlt to Native RAlt",
        },
        {
            "state_key": "rctrl_is_u3",
            "legacy_key": "u3",
            "scan_code": 133,
            "user_code": 238,
            "native_vk": 163,
            "enabled_label": "U3",
            "disabled_label": "RCtrl",
            "enabled_log": "[Info] Switched RCtrl to U3",
            "disabled_log": "[Info] Switched RCtrl to Native RCtrl",
        },
        {
            "state_key": "rshift_is_u4",
            "legacy_key": "u4",
            "scan_code": 134,
            "user_code": 239,
            "native_vk": 161,
            "enabled_label": "U4",
            "disabled_label": "RShift",
            "enabled_log": "[Info] Switched RShift to U4",
            "disabled_log": "[Info] Switched RShift to Native RShift",
        },
    ]
    modifier_states = {
        spec["state_key"]: bool(shared_state.get(spec["state_key"], shared_state.get(spec["legacy_key"], True)))
        for spec in modifier_specs
    }
    def write_keyhac_state(publish=True):
        current_shared_state = read_shared_state()
        komorebi_modal = bool(current_shared_state.get("komorebi_modal", False))
        komorebi_mode_label = "MM" if komorebi_modal else "U1"
        komorebi_mode_color = "#FF7A59" if komorebi_modal else "#66D9EF"
        payload = {
            "komorebi_hotkey_backend": current_shared_state.get("komorebi_hotkey_backend", "kanata"),
            "komorebi_modal": komorebi_modal,
            "komorebi_mode_label": komorebi_mode_label,
            "komorebi_mode_color": komorebi_mode_color,
        }
        for spec in modifier_specs:
            enabled = modifier_states[spec["state_key"]]
            payload[spec["state_key"]] = enabled
            payload[spec["legacy_key"]] = enabled
            payload[f'{spec["legacy_key"]}_label'] = spec["enabled_label"] if enabled else spec["disabled_label"]
        write_shared_state(payload, publish=publish)

    def apply_modifier_mode(spec, enabled, publish=True):
        modifier_states[spec["state_key"]] = enabled
        if enabled:
            keymap.replaceKey(spec["scan_code"], spec["user_code"])
            print(spec["enabled_log"])
        else:
            keymap.replaceKey(spec["scan_code"], spec["native_vk"])
            print(spec["disabled_log"])
        write_keyhac_state(publish=publish)

    def apply_all_modifier_modes(enable_all):
        for index, spec in enumerate(modifier_specs):
            is_last = index == len(modifier_specs) - 1
            apply_modifier_mode(spec, enable_all, publish=is_last)

    def make_toggle_modifier_mode(spec):
        def _toggle_modifier_mode():
            state_key = spec["state_key"]
            apply_modifier_mode(spec, not modifier_states[state_key], publish=True)

        return _toggle_modifier_mode

    def reapply_modifier_modes():
        for index, spec in enumerate(modifier_specs):
            is_last = index == len(modifier_specs) - 1
            apply_modifier_mode(spec, modifier_states[spec["state_key"]], publish=is_last)
    modifier_toggles = {
        spec["state_key"]: make_toggle_modifier_mode(spec)
        for spec in modifier_specs
    }

    def toggle_all_user_modes():
        enable_all = not all(modifier_states[spec["state_key"]] for spec in modifier_specs)
        apply_all_modifier_modes(enable_all)

    reapply_modifier_modes()

    # Global mode toggles use one fixed chord family for easier recall.
    keymap_global["C-A-S-7"] = modifier_toggles["ralt_is_u2"]
    keymap_global["C-A-S-8"] = modifier_toggles["rctrl_is_u3"]
    keymap_global["C-A-S-9"] = modifier_toggles["rshift_is_u4"]
    keymap_global["C-A-S-0"] = modifier_toggles["win_is_u0"]
    keymap_global["C-A-S-Minus"] = modifier_toggles["caps_is_u1"]

    keymap_global["C-S-A-U"] = toggle_all_user_modes
    # Stop modifier + U1 from falling back to native CapsLock when no explicit
    # command should be emitted.
    keymap_global["S-236"] = lambda: None
    keymap_global["W-236"] = lambda: None
    keymap_global["A-236"] = lambda: None

    # --------------------------------------------------------------------
    # 导入并初始化扩展模块
    from extensions.window.list_window_ext import init_list_window_ext, schedule_list_window_search
    from extensions.window.window_switcher import init_window_switcher
    from extensions.clipboard.clipboard_ext import init_clipboard_ext
    from extensions.input.mouse_ext import init_mouse_ext
    from extensions.ui.editor_ext import init_editor_ext
    from extensions.apps.app_launcher import init_app_launcher
    from extensions.tex.texstudio_ext import init_texstudio_ext
    from extensions.ui.coding_ext import init_coding_ext
    from extensions.ui.terminal_matrix_ext import init_terminal_matrix_ext

    init_list_window_ext(keymap)

    # 1. 窗口切换器 (U0 + W)
    init_window_switcher(keymap, keymap_global)

    # 2. 剪贴板历史增强
    init_clipboard_ext(keymap, keymap_global)

    # 3. 鼠标模拟
    init_mouse_ext(keymap, keymap_global)

    # 4. 编辑器增强
    init_editor_ext(keymap)

    # 5. 应用启动器
    init_app_launcher(keymap, keymap_global)

    # 6. TeXstudio 增强 (包含 f-n 扩展热键)
    init_texstudio_ext(keymap)

    # 7. 编程与终端增强 (包含 g-c-p 三键逻辑)
    init_coding_ext(keymap)

    # 8. 终端矩阵启动 (r/g/s-p-7/5)
    init_terminal_matrix_ext(keymap)

    # --------------------------------------------------------------------
    # Windows Terminal 下直接输入命令并回车，绕开输入法对 Ctrl+V 的干扰
    terminal_input_enter_delay_ms = 100

    def command_copy_path_or_copy():
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if hwnd:
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                title = ""
                if length > 0:
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    ctypes.windll.user32.GetWindowTextW(hwnd, buffer, len(buffer))
                    title = buffer.value

                pid = ctypes.c_ulong()
                ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                process_name = ""
                if pid.value:
                    handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid.value)
                    if handle:
                        try:
                            size = ctypes.c_ulong(32768)
                            path_buffer = ctypes.create_unicode_buffer(size.value)
                            if ctypes.windll.kernel32.QueryFullProcessImageNameW(
                                handle, 0, path_buffer, ctypes.byref(size)
                            ):
                                process_name = os.path.basename(path_buffer.value).lower()
                        finally:
                            ctypes.windll.kernel32.CloseHandle(handle)

                is_supported_terminal = process_name in (
                    "wt.exe",
                    "windowsterminal.exe",
                    "rio.exe",
                    "ghostty.exe",
                    "cmd.exe",
                    "powershell.exe",
                    "pwsh.exe",
                )
                if is_supported_terminal:
                    if process_name == "cmd.exe":
                        keymap.InputTextCommand(
                            'powershell -NoProfile -Command "(Get-Location).Path | Set-Clipboard"'
                        )()
                    else:
                        keymap.InputTextCommand("(Get-Location).Path | Set-Clipboard")()
                    keymap.delayedCall(
                        lambda: keymap.InputKeyCommand("Enter")(),
                        terminal_input_enter_delay_ms,
                    )
                    return
        except Exception:
            pass

        keymap.InputKeyCommand("A-D", "C-C")()

    # 常用全局快捷键
    def command_ClipboardListWithSearch():
        keymap.command_ClipboardList()
        schedule_list_window_search(keymap)

    keymap_global["U1-Semicolon"] = command_ClipboardListWithSearch
    keymap_global["U0-0"] = keymap.command_RecordToggle
    keymap_global["U0-3"] = keymap.command_RecordPlay
    keymap_global["U0-C"] = command_copy_path_or_copy

    # 窗口移动快捷键
    keymap_global["U0-Left"]  = keymap.MoveWindowCommand(-10, 0)
    keymap_global["U0-Right"] = keymap.MoveWindowCommand(+10, 0)
    keymap_global["U0-Up"]    = keymap.MoveWindowCommand(0, -10)
    keymap_global["U0-Down"]  = keymap.MoveWindowCommand(0, +10)
