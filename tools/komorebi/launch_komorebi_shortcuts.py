import argparse
import shutil
import subprocess
import sys
from pathlib import Path


EXE_CANDIDATES = [
    Path(r"D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-tauri\src-tauri\target\release\d-c2ddesktopcoderuststoolskomorebi-shortcuts-tauri.exe"),
    Path(r"D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-tauri\src-tauri\target\debug\d-c2ddesktopcoderuststoolskomorebi-shortcuts-tauri.exe"),
    Path(r"D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-tauri\src-tauri\target\release\komorebi-shortcuts-tauri.exe"),
    Path(r"D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-tauri\src-tauri\target\debug\komorebi-shortcuts-tauri.exe"),
    Path(r"D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-slint\target\release\komorebi-shortcuts-slint.exe"),
    Path(r"D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-slint\target\debug\komorebi-shortcuts-slint.exe"),
]

FALLBACK_SCRIPT_CANDIDATES = [
    Path(r"D:\C2D\Desktop\Code\Python\automation\komorebi_config\show_komorebi_shortcuts.py"),
    Path(r"D:\C2D\Desktop\Code\Python\automation\komorebi_config_legacy_hotkeys\shortcuts_py\show_komorebi_shortcuts.py"),
]


def _resolve_existing_path(candidates):
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _get_python_executable(prefer_gui):
    if prefer_gui:
        pythonw = shutil.which("pythonw")
        if pythonw:
            return pythonw

    python = shutil.which("python")
    if python:
        return python

    if sys.executable:
        return sys.executable

    return None


def _launch_executable(exe_path, console):
    if console:
        subprocess.run([str(exe_path)], check=True)
        return

    create_no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    subprocess.Popen([str(exe_path)], creationflags=create_no_window)


def _launch_fallback_script(script_path, backend, start_hidden, console):
    python_exe = _get_python_executable(prefer_gui=not console)
    if not python_exe:
        checked = "; ".join(str(path) for path in EXE_CANDIDATES)
        raise RuntimeError(
            "No komorebi shortcuts executable found, and python/pythonw is not available. "
            f"Checked: {checked}"
        )

    args = [str(script_path), "--backend", backend]
    if start_hidden:
        args.append("--start-hidden")

    if console:
        subprocess.run([python_exe, *args], check=True)
        return

    create_no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    subprocess.Popen([python_exe, *args], creationflags=create_no_window)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--console", action="store_true")
    parser.add_argument("--backend", choices=("kanata", "keyhac", "whkd"), default="kanata")
    parser.add_argument("--start-hidden", action="store_true")
    args = parser.parse_args()

    shortcut_exe = _resolve_existing_path(EXE_CANDIDATES)
    if shortcut_exe:
        _launch_executable(shortcut_exe, args.console)
        return

    fallback_script = _resolve_existing_path(FALLBACK_SCRIPT_CANDIDATES)
    if not fallback_script:
        checked = "; ".join(str(path) for path in EXE_CANDIDATES)
        expected = "; ".join(str(path) for path in FALLBACK_SCRIPT_CANDIDATES)
        raise RuntimeError(
            "No komorebi shortcuts executable found, and fallback script is missing. "
            f"Checked exes: {checked}. Checked scripts: {expected}"
        )

    _launch_fallback_script(fallback_script, args.backend, args.start_hidden, args.console)


if __name__ == "__main__":
    main()
