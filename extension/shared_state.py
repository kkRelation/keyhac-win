import json
import mmap
import os
import struct
import subprocess


MAP_NAME = "Local\\KeyhacSharedState"
MAP_SIZE = 4096
HEADER = struct.Struct("<4sIII")
MAGIC = b"KHSM"
VERSION = 1
BACKEND_ENV = "KOMOREBI_HOTKEY_BACKEND"

DEFAULT_STATE = {
    "win_is_u0": True,
    "caps_is_u1": True,
    "ralt_is_u2": True,
    "rctrl_is_u3": True,
    "rshift_is_u4": True,
    "u0": True,
    "u1": True,
    "u2": True,
    "u3": True,
    "u4": True,
    "u0_label": "U0",
    "u1_label": "U1",
    "u2_label": "U2",
    "u3_label": "U3",
    "u4_label": "U4",
    "komorebi_hotkey_backend": "kanata",
    "komorebi_modal": False,
    "komorebi_mode_label": "U1",
    "komorebi_mode_color": "#66D9EF",
}

_shared_state = None
_shared_map = None
_state_center_exe = r"D:\C2D\Desktop\Code\Python\automation\state_center\target\release\state-client.exe"
_last_published_payload = None


def _initial_state():
    state = dict(DEFAULT_STATE)
    backend = (os.environ.get(BACKEND_ENV) or "kanata").strip().lower()
    state["komorebi_hotkey_backend"] = backend or "kanata"
    return state


def _ensure_state():
    global _shared_state
    if _shared_state is None:
        _shared_state = _initial_state()
    return _shared_state


def _ensure_map():
    global _shared_map
    if _shared_map is None:
        _shared_map = mmap.mmap(-1, MAP_SIZE, tagname=MAP_NAME, access=mmap.ACCESS_WRITE)
    return _shared_map


def _read_map_state():
    try:
        mapping = _ensure_map()
        mapping.seek(0)
        header = mapping.read(HEADER.size)
        if len(header) != HEADER.size:
            return {}

        magic, version, _writer_pid, payload_len = HEADER.unpack(header)
        if magic != MAGIC or version != VERSION:
            return {}

        max_payload = MAP_SIZE - HEADER.size
        if payload_len <= 0 or payload_len > max_payload:
            return {}

        payload = mapping.read(payload_len)
        parsed = json.loads(payload.decode("utf-8"))
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def read_shared_state():
    state = _initial_state()
    state.update(_read_map_state())
    cached = _ensure_state()
    cached.update(state)
    return dict(cached)


def write_shared_state(updates, publish=True):
    global _shared_state
    state = _initial_state()
    state.update(_read_map_state())
    state.update(_ensure_state())
    state.update(updates)
    _shared_state = state

    payload = json.dumps(state, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    header_size = HEADER.size
    max_payload = MAP_SIZE - header_size
    if len(payload) > max_payload:
        raise ValueError("shared state payload exceeds mmap capacity")

    mapping = _ensure_map()
    mapping.seek(0)
    mapping.write(HEADER.pack(MAGIC, VERSION, os.getpid(), len(payload)))
    mapping.write(payload)
    if len(payload) < max_payload:
        mapping.write(b"\x00" * (max_payload - len(payload)))
    mapping.flush()
    if publish:
        _publish_state_center(state)


def _publish_state_center(state):
    global _last_published_payload
    if not os.path.exists(_state_center_exe):
        return

    try:
        payload = json.dumps(state, ensure_ascii=False, separators=(",", ":"))
        if payload == _last_published_payload:
            return
        create_no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        subprocess.Popen(
            [
                _state_center_exe,
                "patch-json",
                "--source",
                "keyhac",
                payload,
            ],
            creationflags=create_no_window,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
        _last_published_payload = payload
    except Exception:
        pass
