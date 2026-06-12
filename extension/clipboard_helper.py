from .clipboard_commands import (
    make_copy_selection_before_passthrough_command,
    make_guarded_clipboard_command,
    make_paste_text_without_history_command,
    make_pre_action_then_input_command,
    probe_selection_via_clipboard_copy,
    register_copy_selection_before_passthrough_combo,
    register_pre_action_passthrough_combo,
    wait_for_clipboard_change,
)
from .key_inject import direct_inject_keys
from .texstudio_commands import (
    make_texstudio_color_command,
    make_texstudio_smart_insert_command,
)
