import ctypes
import json
import os
import shutil
import subprocess
import time
from ctypes import wintypes


DEFAULT_KOMOREBI_CONFIG_DIR = r"D:\C2D\Desktop\Code\Python\automation\komorebi_config"


class KomorebiBarController:
    def __init__(self, config_dir, create_no_window):
        self.config_dir = config_dir
        self.komorebi_config_path = os.path.join(config_dir, "komorebi.json")
        self.bar_state_path = os.path.join(config_dir, "komorebi.bar.state.json")
        self.bar_cache_path = os.path.join(config_dir, "komorebi.bar.window-cache.json")
        self.create_no_window = create_no_window
        self.komorebi_bar_path = (
            r"E:\Scoop\apps\komorebi\current\komorebi-bar.exe"
            if os.path.exists(r"E:\Scoop\apps\komorebi\current\komorebi-bar.exe")
            else (shutil.which("komorebi-bar") or "komorebi-bar")
        )
        self.bar_window_cache = {}

        self.user32 = ctypes.WinDLL("user32", use_last_error=True)
        self.enum_windows_proc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        self.user32.EnumWindows.argtypes = [self.enum_windows_proc, wintypes.LPARAM]
        self.user32.EnumWindows.restype = wintypes.BOOL
        self.user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
        self.user32.GetWindowThreadProcessId.restype = wintypes.DWORD
        self.user32.IsWindow.argtypes = [wintypes.HWND]
        self.user32.IsWindow.restype = wintypes.BOOL
        self.user32.IsWindowVisible.argtypes = [wintypes.HWND]
        self.user32.IsWindowVisible.restype = wintypes.BOOL
        self.user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
        self.user32.ShowWindow.restype = wintypes.BOOL
        self.user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
        self.user32.GetWindowTextLengthW.restype = ctypes.c_int
        self.user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
        self.user32.GetWindowTextW.restype = ctypes.c_int

        self._sw_hide = 0
        self._sw_show_no_activate = 4
        self._load_bar_window_cache()

    def _load_bar_window_cache(self):
        if not os.path.exists(self.bar_cache_path):
            self.bar_window_cache = {}
            return

        try:
            with open(self.bar_cache_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                self.bar_window_cache = data
            else:
                self.bar_window_cache = {}
        except Exception:
            self.bar_window_cache = {}

    def _save_bar_window_cache(self):
        try:
            with open(self.bar_cache_path, "w", encoding="utf-8") as handle:
                json.dump(self.bar_window_cache, handle, ensure_ascii=False)
        except Exception:
            pass

    def process_is_running(self, pid):
        try:
            completed = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                creationflags=self.create_no_window,
                check=False,
            )
            output = (completed.stdout or "").strip()
            return bool(output) and "No tasks are running" not in output
        except Exception:
            return False

    def hwnd_is_valid(self, hwnd):
        return bool(hwnd) and bool(self.user32.IsWindow(wintypes.HWND(int(hwnd))))

    def hwnd_is_visible(self, hwnd):
        return self.hwnd_is_valid(hwnd) and bool(self.user32.IsWindowVisible(wintypes.HWND(int(hwnd))))

    def set_window_visibility(self, hwnd, visible):
        if not self.hwnd_is_valid(hwnd):
            return False

        command = self._sw_show_no_activate if visible else self._sw_hide
        self.user32.ShowWindow(wintypes.HWND(int(hwnd)), command)
        return True

    def get_hwnds_for_pid(self, pid):
        hwnds = []

        @self.enum_windows_proc
        def _callback(hwnd, _lparam):
            process_id = wintypes.DWORD()
            self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
            if int(process_id.value) == int(pid):
                hwnds.append(int(hwnd))
            return True

        self.user32.EnumWindows(_callback, 0)
        return hwnds

    def get_window_title(self, hwnd):
        if not self.hwnd_is_valid(hwnd):
            return ""

        length = self.user32.GetWindowTextLengthW(wintypes.HWND(int(hwnd)))
        buffer = ctypes.create_unicode_buffer(max(length + 1, 256))
        self.user32.GetWindowTextW(wintypes.HWND(int(hwnd)), buffer, len(buffer))
        return buffer.value or ""

    def get_bar_configurations(self):
        if not os.path.exists(self.komorebi_config_path):
            return []

        try:
            with open(self.komorebi_config_path, "r", encoding="utf-8-sig") as handle:
                config = json.load(handle)
        except Exception:
            return []

        bar_configs = []
        for bar_config_path in config.get("bar_configurations", []):
            try:
                with open(bar_config_path, "r", encoding="utf-8-sig") as handle:
                    bar_config = json.load(handle)
                bar_configs.append({
                    "path": bar_config_path,
                    "monitor": int(bar_config.get("monitor", -1)),
                })
            except Exception:
                continue

        return bar_configs

    def get_bar_cache_entry(self, bar_config_path):
        entry = self.bar_window_cache.get(bar_config_path)
        if not isinstance(entry, dict):
            entry = None

        if entry:
            pid = int(entry.get("pid", 0) or 0)
            hwnd = int(entry.get("hwnd", 0) or 0)
            if pid > 0 and self.process_is_running(pid) and self.hwnd_is_valid(hwnd):
                return {"pid": pid, "hwnd": hwnd}

            self.bar_window_cache.pop(bar_config_path, None)
            self._save_bar_window_cache()

        completed = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                (
                    "Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | "
                    "Where-Object { $_.Name -eq 'komorebi-bar.exe' -and $_.CommandLine -like '*"
                    + bar_config_path.replace("'", "''")
                    + "*' } | ForEach-Object { '{0},{1}' -f $_.ProcessId, $_.ParentProcessId }"
                ),
            ],
            capture_output=True,
            text=True,
            creationflags=self.create_no_window,
            check=False,
        )

        process_pairs = []
        for line in (completed.stdout or "").splitlines():
            line = line.strip()
            if not line:
                continue

            parts = [part.strip() for part in line.split(",", 1)]
            if len(parts) != 2:
                continue

            try:
                pid = int(parts[0])
                parent_pid = int(parts[1])
            except ValueError:
                continue

            process_pairs.append({"pid": pid, "parent_pid": parent_pid})

        if not process_pairs:
            return None

        parent_ids = {item["parent_pid"] for item in process_pairs if item["parent_pid"] > 0}
        leaf_pairs = [item for item in process_pairs if item["pid"] not in parent_ids]
        if not leaf_pairs:
            leaf_pairs = process_pairs

        preferred_pairs = []
        fallback_pairs = []
        for item in leaf_pairs:
            pid = item["pid"]
            if not self.process_is_running(pid):
                continue

            hwnds = [hwnd for hwnd in self.get_hwnds_for_pid(pid) if self.hwnd_is_valid(hwnd)]
            if not hwnds:
                continue

            visible_hwnds = [hwnd for hwnd in hwnds if self.hwnd_is_visible(hwnd)]
            if visible_hwnds:
                preferred_pairs.append({"pid": pid, "hwnd": visible_hwnds[0]})
            else:
                fallback_pairs.append({"pid": pid, "hwnd": hwnds[0]})

        for candidate in preferred_pairs + fallback_pairs:
            self.bar_window_cache[bar_config_path] = candidate
            self._save_bar_window_cache()
            return {"pid": candidate["pid"], "hwnd": candidate["hwnd"]}

        return None

    def scan_bar_entry_for_process(self, process):
        pid = int(process.pid)
        deadline = time.time() + 3.0

        while time.time() < deadline and self.process_is_running(pid):
            hwnds = self.get_hwnds_for_pid(pid)
            visible_hwnds = [hwnd for hwnd in hwnds if self.hwnd_is_visible(hwnd)]
            if visible_hwnds:
                return {"pid": pid, "hwnd": visible_hwnds[0]}

            titled_hwnds = [hwnd for hwnd in hwnds if self.get_window_title(hwnd)]
            if titled_hwnds:
                return {"pid": pid, "hwnd": titled_hwnds[0]}

            time.sleep(0.05)

        return None

    def start_bar_process(self, bar_config_path):
        process = subprocess.Popen(
            [self.komorebi_bar_path, "--config", bar_config_path],
            creationflags=self.create_no_window,
        )
        entry = self.scan_bar_entry_for_process(process)
        if entry:
            self.bar_window_cache[bar_config_path] = entry
            self._save_bar_window_cache()
            return entry

        return None

    def show_bar_for_config(self, bar_config_path):
        entry = self.get_bar_cache_entry(bar_config_path)
        if entry:
            if self.set_window_visibility(entry["hwnd"], True):
                return True

            self.bar_window_cache.pop(bar_config_path, None)
            self._save_bar_window_cache()

        entry = self.start_bar_process(bar_config_path)
        return entry is not None

    def hide_bar_for_config(self, bar_config_path):
        entry = self.get_bar_cache_entry(bar_config_path)
        if entry and self.set_window_visibility(entry["hwnd"], False):
            return True

        if entry:
            self.bar_window_cache.pop(bar_config_path, None)
            self._save_bar_window_cache()

        return True

    def read_hidden_monitors(self):
        if not os.path.exists(self.bar_state_path):
            return []

        try:
            with open(self.bar_state_path, "r", encoding="utf-8-sig") as handle:
                state = json.load(handle)
            return sorted({int(item) for item in state.get("hidden_bar_monitors", [])})
        except Exception:
            return []

    def write_hidden_monitors(self, hidden_monitors):
        with open(self.bar_state_path, "w", encoding="utf-8") as handle:
            json.dump({"hidden_bar_monitors": hidden_monitors}, handle, ensure_ascii=False)

    def apply_hidden_monitor_state(self, hidden_monitors):
        for bar_config in self.get_bar_configurations():
            should_be_visible = bar_config["monitor"] not in hidden_monitors
            if should_be_visible:
                self.show_bar_for_config(bar_config["path"])
            else:
                self.hide_bar_for_config(bar_config["path"])

    def make_toggle_bar_monitor_command(self, monitor):
        def _command():
            try:
                hidden_monitors = self.read_hidden_monitors()
                if monitor in hidden_monitors:
                    hidden_monitors = [item for item in hidden_monitors if item != monitor]
                else:
                    hidden_monitors = sorted(set(hidden_monitors + [monitor]))

                self.write_hidden_monitors(hidden_monitors)
                self.apply_hidden_monitor_state(hidden_monitors)
            except Exception as exc:
                print(f"[komorebi_ext] Failed to toggle bar monitor {monitor}: {exc}")

        return _command


def make_detached_command_runner(create_no_window):
    def _run_detached(command):
        def _command():
            try:
                subprocess.Popen(command, creationflags=create_no_window)
            except Exception as exc:
                print(f"[komorebi_ext] Failed to start {' '.join(command)}: {exc}")

        return _command

    return _run_detached


def build_komorebi_bindings(keymap, komorebic, modal_enabled, toggle_bar_monitor):
    # Pure komorebic bindings now live in Kanata so printable combos and modal
    # keys can be intercepted at the physical-key layer with lower latency.
    return {}
