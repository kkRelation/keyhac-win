from extensions.clipboard.clipboard_commands import (
    make_guarded_clipboard_command,
    make_paste_text_without_history_command,
    probe_selection_via_clipboard_copy,
)


def make_texstudio_smart_insert_command(keymap, prefix, suffix):
    def _command():
        def _finish(selected, _copied, previous_clipboard):
            if selected:
                make_paste_text_without_history_command(
                    keymap,
                    prefix + selected + suffix,
                    original_clipboard=previous_clipboard,
                )()
            else:
                post_keys = ["Left"] * len(suffix)
                make_paste_text_without_history_command(
                    keymap,
                    prefix + suffix,
                    post_keys,
                    original_clipboard=previous_clipboard,
                )()

        probe_selection_via_clipboard_copy(keymap, _finish, restore_if_failed=False)

    return _command


def make_texstudio_color_command(keymap, color_name):
    return make_texstudio_smart_insert_command(keymap, rf"\textcolor{{{color_name}}}{{", "}")


def make_texstudio_bracket_clipboard_command(keymap, bracket_key, clipboard_key, delay_ms=200):
    guarded_clipboard = make_guarded_clipboard_command(keymap, clipboard_key)

    def _command():
        keymap.InputKeyCommand(bracket_key)()
        keymap.delayedCall(guarded_clipboard, delay_ms)

    return _command


def make_texstudio_bracket_paste_command(keymap, bracket_key, delay_ms=200):
    def _command():
        keymap.InputKeyCommand(bracket_key)()
        keymap.delayedCall(keymap.InputKeyCommand("C-V"), delay_ms)

    return _command
