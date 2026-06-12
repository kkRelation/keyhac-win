import os
import subprocess
import shutil
import ctypes
import time
import base64
from ctypes import wintypes
from keyhac import *

from extensions.input.powerkey_ext import PowerKeyManager
from extensions.input.key_inject import direct_inject_keys


_CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
_WT_EXE_CACHE = None
_WT_DIRECT_EXE_CACHE = None
_PS5_PROFILE_PATH = r"D:\C2D\Documents\WindowsPowerShell\profile.ps1"

_SHELL_COMMANDS = {
    "ps7": ["pwsh", "-NoLogo"],
}

_WT_PROFILE_BY_SHELL = {
    "ps7": "{9f986cf1-261a-4f88-9f66-a2d0ce5f4b8e}",
    "ps5": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
}

_GHOSTTY_CONFIG_PATH = r"E:\MCP\Projects\ghostty-windows\config\config"
_GHOSTTY_CONFIG_BY_SHELL = {
    "ps5": r"E:\MCP\Projects\ghostty-windows\config\config.ps5",
    "ps7": r"E:\MCP\Projects\ghostty-windows\config\config.ps7",
}
_RIO_CONFIG_HOME = r"D:\C2D\dotfiles\rio"
_RIO_CONFIG_PATH = os.path.join(_RIO_CONFIG_HOME, "config.toml")

_TERMINAL_COMMANDS = {
    "native": lambda shell_cmd, launch_dir: shell_cmd,
    "rio": lambda shell_cmd, launch_dir: ["rio", "-w", launch_dir, "-e"] + shell_cmd,
    "ghostty": lambda shell_cmd, launch_dir: [
        "ghostty",
        f"--working-directory={launch_dir}",
        f"--config-file={_GHOSTTY_CONFIG_PATH}",
        "-e",
    ] + shell_cmd,
}

_TERMINAL_PREFIX_MATRIX = {
    "s": ("native", {"p-7": "ps7", "p-5": "ps5"}),
    "r": ("rio", {"p-7": "ps7", "p-5": "ps5"}),
    "g": ("ghostty", {"p-7": "ps7", "p-5": "ps5"}),
}

_EXPLORER_TITLE_SUFFIXES = (
    " - 文件资源管理器",
    " - File Explorer",
)

_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32

_user32.GetForegroundWindow.restype = wintypes.HWND
_user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
_user32.GetWindowTextLengthW.restype = ctypes.c_int
_user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
_user32.GetWindowTextW.restype = ctypes.c_int
_user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
_user32.GetWindowThreadProcessId.restype = wintypes.DWORD
_kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
_kernel32.OpenProcess.restype = wintypes.HANDLE
_kernel32.QueryFullProcessImageNameW.argtypes = [
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.LPWSTR,
    ctypes.POINTER(wintypes.DWORD),
]
_kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
_kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
_kernel32.CloseHandle.restype = wintypes.BOOL

_PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
_ERROR_ACCESS_DENIED = 5
_ERROR_FILE_INACCESSIBLE = 1920


def _get_window_text(hwnd):
    length = _user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return ""
    buffer = ctypes.create_unicode_buffer(length + 1)
    _user32.GetWindowTextW(hwnd, buffer, len(buffer))
    return buffer.value


def _get_process_name(hwnd):
    process_id = wintypes.DWORD()
    _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
    if not process_id.value:
        return ""

    handle = _kernel32.OpenProcess(
        _PROCESS_QUERY_LIMITED_INFORMATION,
        False,
        process_id.value,
    )
    if not handle:
        return ""

    try:
        size = wintypes.DWORD(32768)
        buffer = ctypes.create_unicode_buffer(size.value)
        if not _kernel32.QueryFullProcessImageNameW(
            handle,
            0,
            buffer,
            ctypes.byref(size),
        ):
            return ""
        return os.path.basename(buffer.value).lower()
    finally:
        _kernel32.CloseHandle(handle)


def _path_from_explorer_title(title):
    title = (title or "").strip()
    for suffix in _EXPLORER_TITLE_SUFFIXES:
        if title.endswith(suffix):
            candidate = title[:-len(suffix)].strip()
            if os.path.isdir(candidate):
                return candidate
    if os.path.isdir(title):
        return title
    return ""


def _copy_explorer_address_bar_path():
    previous_clipboard = ""
    try:
        previous_clipboard = getClipboardText()
    except Exception:
        pass

    try:
        setClipboardText("")
        direct_inject_keys("A-D")
        time.sleep(0.06)
        direct_inject_keys("C-C")
        time.sleep(0.10)
        path = getClipboardText().strip()
        if os.path.isdir(path):
            return path
    except Exception:
        return ""
    finally:
        try:
            setClipboardText(previous_clipboard)
        except Exception:
            pass
    return ""


def _get_explorer_path():
    hwnd = _user32.GetForegroundWindow()
    if not hwnd or _get_process_name(hwnd) != "explorer.exe":
        return ""

    path = _path_from_explorer_title(_get_window_text(hwnd))
    if path:
        return path

    return _copy_explorer_address_bar_path()


def _remember_path_for_zoxide(path):
    zoxide_exe = shutil.which("zoxide")
    if not zoxide_exe:
        return
    try:
        subprocess.Popen(
            [zoxide_exe, "add", path],
            creationflags=_CREATE_NO_WINDOW,
        )
    except Exception:
        pass


def _resolve_wt_exe():
    global _WT_EXE_CACHE
    if _WT_EXE_CACHE is not None:
        return _WT_EXE_CACHE

    windows_apps_wt = os.path.join(
        os.path.expandvars(r"%LOCALAPPDATA%"),
        "Microsoft",
        "WindowsApps",
        "wt.exe",
    )
    if os.path.exists(windows_apps_wt):
        _WT_EXE_CACHE = windows_apps_wt
        return _WT_EXE_CACHE

    wt_exe = shutil.which("wt")
    if wt_exe:
        _WT_EXE_CACHE = wt_exe
        return _WT_EXE_CACHE

    _WT_EXE_CACHE = ""
    return _WT_EXE_CACHE


def _resolve_wt_direct_exe():
    global _WT_DIRECT_EXE_CACHE
    if _WT_DIRECT_EXE_CACHE is not None:
        return _WT_DIRECT_EXE_CACHE
    try:
        probe = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-AppxPackage -Name Microsoft.WindowsTerminal).InstallLocation",
            ],
            capture_output=True,
            text=True,
            creationflags=_CREATE_NO_WINDOW,
        )
        install_dir = (probe.stdout or "").strip()
        if install_dir:
            direct_exe = os.path.join(install_dir, "WindowsTerminal.exe")
            if os.path.exists(direct_exe):
                _WT_DIRECT_EXE_CACHE = direct_exe
                return _WT_DIRECT_EXE_CACHE
    except Exception:
        pass
    _WT_DIRECT_EXE_CACHE = ""
    return _WT_DIRECT_EXE_CACHE


def _get_shell_command(shell_kind):
    if shell_kind == "ps5":
        # Inline startup logic and pass it via EncodedCommand to avoid wt ';' parsing issues.
        if os.path.exists(_PS5_PROFILE_PATH):
            startup_script = (
                ". '{}'\n"
                "if (Get-Command Set-PSReadLineOption -ErrorAction SilentlyContinue) {{\n"
                "    Set-PSReadLineOption -ContinuationPrompt '> '\n"
                "    Set-PSReadLineOption -Colors @{{ ContinuationPrompt = [ConsoleColor]::DarkGray }}\n"
                "}}\n"
            ).format(_PS5_PROFILE_PATH)
            encoded = base64.b64encode(startup_script.encode("utf-16le")).decode("ascii")
            return [
                "powershell",
                "-NoLogo",
                "-NoProfile",
                "-NoExit",
                "-ExecutionPolicy",
                "Bypass",
                "-EncodedCommand",
                encoded,
            ]
        return ["powershell", "-NoLogo"]

    return _SHELL_COMMANDS[shell_kind]


def _is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _start_native_fallback_via_cmd(wt_exe, wt_profile, launch_dir, shell_cmd):
    # Use cmd start to trigger app execution alias path in a separate process context.
    quoted = subprocess.list2cmdline(
        [wt_exe, "new-tab", "-p", wt_profile, "-d", launch_dir] + shell_cmd
    )
    return subprocess.Popen(
        ["cmd.exe", "/c", "start", "", quoted],
        cwd=launch_dir,
        creationflags=_CREATE_NO_WINDOW,
    )


def _is_recoverable_native_error(exc):
    if not isinstance(exc, OSError):
        return False
    return getattr(exc, "winerror", None) in (_ERROR_ACCESS_DENIED, _ERROR_FILE_INACCESSIBLE)


def _build_wt_candidates():
    candidates = []
    primary = _resolve_wt_exe()
    direct = _resolve_wt_direct_exe()
    for value in (primary, "wt.exe", "wt", direct):
        if value and value not in candidates:
            candidates.append(value)
    return candidates


def _launch_terminal(terminal_kind, shell_kind):
    shell_cmd = _get_shell_command(shell_kind)
    launch_dir = _get_explorer_path() or os.path.expanduser("~")
    _remember_path_for_zoxide(launch_dir)
    command = _TERMINAL_COMMANDS[terminal_kind](shell_cmd, launch_dir)
    if terminal_kind == "ghostty":
        ghostty_config = _GHOSTTY_CONFIG_BY_SHELL.get(shell_kind, _GHOSTTY_CONFIG_PATH)
        command[2] = f"--config-file={ghostty_config}"
        if shell_kind == "ps5":
            # Force command on CLI (higher priority than config command) to avoid startup-chain drift.
            command = [
                "ghostty",
                f"--working-directory={launch_dir}",
                f"--config-file={ghostty_config}",
                "--command=" + subprocess.list2cmdline(shell_cmd),
            ]
    env = None
    if terminal_kind == "rio":
        env = os.environ.copy()
        env["RIO_CONFIG_HOME"] = _RIO_CONFIG_HOME
        env["RIO_CONFIG"] = _RIO_CONFIG_PATH
    try:
        if terminal_kind == "native":
            wt_profile = _WT_PROFILE_BY_SHELL.get(shell_kind)
            wt_candidates = _build_wt_candidates()
            if not wt_candidates:
                raise FileNotFoundError("Windows Terminal (wt) not found")

            launched = False
            last_error = None
            for wt_exe in wt_candidates:
                wt_cmd = [wt_exe, "new-tab", "-p", wt_profile, "-d", launch_dir] + shell_cmd
                try:
                    subprocess.Popen(wt_cmd, cwd=launch_dir)
                    launched = True
                    break
                except Exception as e:
                    if _is_recoverable_native_error(e):
                        last_error = e
                        print(
                            "[terminal_matrix_ext] native launch recoverable failure; trying next wt candidate "
                            f"(admin={_is_admin()}, wt={wt_exe}, cwd={launch_dir}, winerror={getattr(e, 'winerror', None)})"
                        )
                        try:
                            _start_native_fallback_via_cmd(wt_exe, wt_profile, launch_dir, shell_cmd)
                            launched = True
                            break
                        except Exception as cmd_e:
                            if _is_recoverable_native_error(cmd_e):
                                last_error = cmd_e
                                continue
                            raise
                    else:
                        raise
            if not launched:
                # Keep ps5/ps7 isolated when wt is fully unavailable.
                subprocess.Popen(shell_cmd, cwd=launch_dir)
                print(
                    "[terminal_matrix_ext] all wt candidates failed; fallback to shell only "
                    f"(shell={shell_kind}, admin={_is_admin()}, cwd={launch_dir}, last_error={last_error})"
                )
        else:
            subprocess.Popen(
                command,
                cwd=launch_dir,
                env=env,
                creationflags=_CREATE_NO_WINDOW,
            )
    except Exception as e:
        print(
            "[terminal_matrix_ext] launch failed "
            f"({terminal_kind}/{shell_kind}): {e}; "
            f"admin={_is_admin()}, cwd={launch_dir}, cmd={command}"
        )


def _defer_launch_terminal(keymap, terminal_kind, shell_kind):
    def _go():
        _launch_terminal(terminal_kind, shell_kind)
    keymap.delayedCall(_go, 0)


def init_terminal_matrix_ext(keymap):
    _keymap_global_pk, pk = PowerKeyManager.for_scope(
        keymap,
        "global:terminal_matrix_ext",
    )

    for prefix, (terminal_kind, sequence_map) in _TERMINAL_PREFIX_MATRIX.items():
        pk.add(
            prefix,
            {
                sequence: (
                    lambda t=terminal_kind, s=shell_kind: _defer_launch_terminal(keymap, t, s)
                )
                for sequence, shell_kind in sequence_map.items()
            },
        )

    pk.finalize()
