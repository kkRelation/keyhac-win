import shutil
import subprocess
import os
from extensions.system.shared_state import read_shared_state
from extensions.apps.komorebi_runtime import (
    build_komorebi_bindings,
)


def init_komorebi_ext(keymap, keymap_global):
    state = read_shared_state()
    mode = (state.get("komorebi_hotkey_backend") or "kanata").strip().lower()

    if mode != "keyhac":
        print(f"[komorebi_ext] Hotkeys disabled because backend is '{mode}'")
        return

    komorebic_path = shutil.which("komorebic") or "komorebic"
    create_no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    def komorebic(*args):
        def _command():
            try:
                subprocess.Popen([komorebic_path, *args], creationflags=create_no_window)
            except Exception as exc:
                print(f"[komorebi_ext] Failed to start {' '.join([komorebic_path, *args])}: {exc}")

        return _command

    bindings = build_komorebi_bindings(
        keymap,
        komorebic,
        lambda: bool(read_shared_state().get("komorebi_modal", False)),
        lambda _monitor: lambda: None,
    )

    for hotkey, command in bindings.items():
        keymap_global[hotkey] = command
