import os
import shutil
import subprocess
from urllib.parse import urlparse

from .powerkey_ext import PowerKeyManager


def _resolve_browser_executable(browser):
    if not browser:
        return None

    expanded = os.path.expandvars(os.path.expanduser(browser))
    if os.path.isabs(expanded) or os.path.sep in expanded or (os.path.altsep and os.path.altsep in expanded):
        return expanded

    return shutil.which(expanded) or browser


def _build_browser_command(url, browser=None, private=False, new_window=True, extra_args=None):
    executable = _resolve_browser_executable(browser)
    if not executable:
        return None

    browser_name = os.path.basename(executable).lower()
    args = [executable]

    if "firefox" in browser_name:
        if private:
            args.append("-private-window")
        elif new_window:
            args.append("-new-window")
        args.append(url)
    elif "chrome" in browser_name or "msedge" in browser_name or "edge" in browser_name:
        if private:
            args.append("--incognito")
        if new_window:
            args.append("--new-window")
        args.append(url)
    else:
        args.append(url)

    if extra_args:
        args.extend(extra_args)

    return args


def make_open_url_command(url, browser=None, private=False, new_window=True, extra_args=None):
    parsed = urlparse(url)
    if not parsed.scheme:
        raise ValueError(f"URL must include a scheme: {url}")

    browser_command = _build_browser_command(
        url,
        browser=browser,
        private=private,
        new_window=new_window,
        extra_args=extra_args,
    )

    def command_OpenUrl():
        if browser_command:
            try:
                subprocess.Popen(browser_command)
                return
            except Exception as exc:
                print(f"[Warn] Failed to launch {browser or 'browser'} for {url}: {exc}")

        os.startfile(url)

    return command_OpenUrl


def register_url_shortcuts(keymap, shortcut_specs, scope_name="global:url-shortcuts"):
    _, powerkey = PowerKeyManager.for_scope(keymap, scope_name)

    for spec in shortcut_specs:
        sequence = spec["sequence"]
        parts = [part for part in str(sequence).split("-") if part]
        if len(parts) < 2:
            raise ValueError(f"Shortcut sequence must contain a prefix and suffix: {sequence}")

        prefix = parts[0]
        suffix = "-".join(parts[1:])
        command = make_open_url_command(
            spec["url"],
            browser=spec.get("browser"),
            private=spec.get("private", False),
            new_window=spec.get("new_window", True),
            extra_args=spec.get("extra_args"),
        )
        powerkey.add(prefix, {suffix: command})

    powerkey.finalize()
