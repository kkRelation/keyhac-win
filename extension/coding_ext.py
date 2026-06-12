from keyhac import *
from .powerkey_ext import PowerKeyManager
from .snippet_sequences import add_fork_sequence, add_git_commit_sequence, add_resume_sequence


def init_coding_ext(keymap):
    _keymap_global_pk, pk = PowerKeyManager.for_scope(
        keymap,
        "global:coding_ext",
    )
    add_git_commit_sequence(keymap, pk)
    add_resume_sequence(keymap, pk)
    add_fork_sequence(keymap, pk)

    pk.finalize()
