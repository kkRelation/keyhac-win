from keyhac import *
from extensions.input.powerkey_ext import PowerKeyManager
from extensions.ui.snippet_sequences import (
    ENABLE_FORK_SEQUENCE,
    ENABLE_RESUME_SEQUENCE,
    add_fork_sequence,
    add_git_commit_sequence,
    add_resume_sequence,
    add_translate_prompt_sequence,
)


def init_coding_ext(keymap):
    _keymap_global_pk, pk = PowerKeyManager.for_scope(
        keymap,
        "global:coding_ext",
    )
    add_git_commit_sequence(keymap, pk)
    if ENABLE_RESUME_SEQUENCE:
        add_resume_sequence(keymap, pk)
    if ENABLE_FORK_SEQUENCE:
        add_fork_sequence(keymap, pk)
    add_translate_prompt_sequence(keymap, pk)

    pk.finalize()
