from keyhac import *

from .key_inject import direct_inject_keys


_SELECTION_SENTINEL = "\x00__PK_SENTINEL__\x00"


def _set_clipboard_text_silently(keymap, text):
    keymap.clipboard_history.enableHook(False)
    try:
        setClipboardText(text)
    finally:
        keymap.clipboard_history.enableHook(True)


def wait_for_clipboard_change(
    keymap,
    baseline_text,
    on_done,
    timeout_ms=300,
    poll_interval_ms=15,
):
    def _do_wait(job_item):
        import time

        deadline = time.time() + timeout_ms / 1000.0
        while time.time() < deadline:
            try:
                clipboard_text = getClipboardText()
            except Exception:
                clipboard_text = None
            if clipboard_text and clipboard_text != baseline_text:
                job_item.changed = True
                job_item.clipboard_text = clipboard_text
                return
            time.sleep(poll_interval_ms / 1000.0)
        try:
            clipboard_text = getClipboardText()
        except Exception:
            clipboard_text = None
        job_item.changed = bool(clipboard_text and clipboard_text != baseline_text)
        job_item.clipboard_text = clipboard_text or ""

    def _finish(job_item):
        on_done(job_item.clipboard_text, job_item.changed)

    JobQueue.defaultQueue().enqueue(JobItem(_do_wait, _finish))


def probe_selection_via_clipboard_copy(
    keymap,
    on_done,
    copy_key="C-C",
    timeout_ms=300,
    poll_interval_ms=15,
    restore_if_failed=True,
):
    def _worker(job_item):
        job_item.previous_clipboard = getClipboardText()
        try:
            _set_clipboard_text_silently(keymap, _SELECTION_SENTINEL)
        except Exception:
            job_item.failed = True

    def _worker_done(job_item):
        if getattr(job_item, "failed", False):
            on_done("", False, getattr(job_item, "previous_clipboard", None))
            return

        def do_copy():
            direct_inject_keys(copy_key)

            def _after_wait(clipboard_text, changed):
                copied = changed and clipboard_text != _SELECTION_SENTINEL

                def _settled_done():
                    if not copied and restore_if_failed:
                        def _restore_worker(job):
                            try:
                                _set_clipboard_text_silently(keymap, job_item.previous_clipboard or "")
                            except Exception:
                                pass

                        JobQueue.defaultQueue().enqueue(JobItem(_restore_worker, lambda _job: None))

                    on_done(
                        clipboard_text if copied else "",
                        copied,
                        job_item.previous_clipboard,
                    )

                keymap.delayedCall(_settled_done, 50)

            wait_for_clipboard_change(
                keymap,
                _SELECTION_SENTINEL,
                _after_wait,
                timeout_ms=timeout_ms,
                poll_interval_ms=poll_interval_ms,
            )

        keymap.delayedCall(do_copy, 30)

    JobQueue.defaultQueue().enqueue(JobItem(_worker, _worker_done))


def make_pre_action_then_input_command(keymap, passthrough_keys, before_passthrough=None):
    if isinstance(passthrough_keys, str):
        keys = [passthrough_keys]
    else:
        keys = list(passthrough_keys)

    is_running = [False]

    def _send_passthrough():
        try:
            for key in keys:
                direct_inject_keys(key)
        finally:
            is_running[0] = False

    def _command():
        if is_running[0]:
            return
        is_running[0] = True

        try:
            if before_passthrough is None:
                _send_passthrough()
            else:
                before_passthrough(_send_passthrough)
        except Exception:
            is_running[0] = False
            raise

    return _command


def register_pre_action_passthrough_combo(window_keymap, combo, command_factory):
    window_keymap[combo] = command_factory(combo)


def make_copy_selection_before_passthrough_command(
    keymap,
    passthrough_keys,
    copy_key="C-C",
    timeout_ms=300,
    poll_interval_ms=15,
):
    def _before_passthrough(send_passthrough):
        probe_selection_via_clipboard_copy(
            keymap,
            lambda _selection, _copied, _previous: send_passthrough(),
            copy_key=copy_key,
            timeout_ms=timeout_ms,
            poll_interval_ms=poll_interval_ms,
        )

    return make_pre_action_then_input_command(
        keymap,
        passthrough_keys,
        before_passthrough=_before_passthrough,
    )


def register_copy_selection_before_passthrough_combo(
    keymap,
    window_keymap,
    combo,
    copy_key="C-C",
    timeout_ms=300,
    poll_interval_ms=15,
):
    def _factory(passthrough_combo):
        return make_copy_selection_before_passthrough_command(
            keymap,
            passthrough_combo,
            copy_key=copy_key,
            timeout_ms=timeout_ms,
            poll_interval_ms=poll_interval_ms,
        )

    register_pre_action_passthrough_combo(window_keymap, combo, _factory)


def make_paste_text_without_history_command(
    keymap,
    text,
    post_keys=None,
    paste_delay_ms=100,
    restore_delay_ms=200,
    original_clipboard=None,
):
    is_running = [False]

    def _command():
        if is_running[0]:
            return
        is_running[0] = True

        def _worker(job_item):
            job_item.previous_clipboard = original_clipboard if original_clipboard is not None else getClipboardText()
            try:
                _set_clipboard_text_silently(keymap, text)
            except Exception:
                job_item.failed = True

        def _worker_done(job_item):
            if getattr(job_item, "failed", False):
                try:
                    _set_clipboard_text_silently(keymap, getattr(job_item, "previous_clipboard", "") or "")
                finally:
                    is_running[0] = False
                return

            def do_paste():
                direct_inject_keys("C-V")

                def restore_clipboard():
                    def _restore_worker(job):
                        try:
                            _set_clipboard_text_silently(keymap, job_item.previous_clipboard or "")
                        except Exception:
                            pass

                    def _restore_done(job):
                        is_running[0] = False

                    JobQueue.defaultQueue().enqueue(JobItem(_restore_worker, _restore_done))

                if post_keys:
                    def send_post_keys():
                        for key in post_keys:
                            direct_inject_keys(key)

                    keymap.delayedCall(send_post_keys, paste_delay_ms)
                    keymap.delayedCall(restore_clipboard, restore_delay_ms)
                else:
                    keymap.delayedCall(restore_clipboard, paste_delay_ms)

            keymap.delayedCall(do_paste, paste_delay_ms)

        JobQueue.defaultQueue().enqueue(JobItem(_worker, _worker_done))

    return _command


def make_guarded_clipboard_command(
    keymap,
    clipboard_key,
    on_done=None,
    timeout_ms=300,
    poll_interval_ms=15,
):
    is_running = [False]

    def _command():
        if is_running[0]:
            return
        is_running[0] = True

        def _finish(selected, copied, previous):
            try:
                if on_done:
                    on_done(selected, copied, previous)
            finally:
                is_running[0] = False

        probe_selection_via_clipboard_copy(
            keymap,
            _finish,
            copy_key=clipboard_key,
            timeout_ms=timeout_ms,
            poll_interval_ms=poll_interval_ms,
        )

    return _command
