from keyhac import *
from .texstudio_commands import (
    make_texstudio_bracket_clipboard_command,
    make_texstudio_bracket_paste_command,
    make_texstudio_color_command,
    make_texstudio_smart_insert_command,
)
from .powerkey_ext import PowerKeyManager
from .snippet_sequences import add_git_commit_sequence


def init_texstudio_ext(keymap):
    # TeXstudio-specific keymap
    keymap_texstudio, pk_tex = PowerKeyManager.for_scope(
        keymap,
        "exe:texstudio.exe",
        exe_name="texstudio.exe",
    )
    pk_tex.add("f", {
        "n": make_texstudio_smart_insert_command(keymap, r"\Footnote{", "}")
    })

    # Color shortcuts
    pk_tex.add("n", {
        "b": make_texstudio_color_command(keymap, "NavyBlue")
    })
    pk_tex.add("m", {
        "r": make_texstudio_color_command(keymap, "Maroon")
    })
    pk_tex.add("p", {
        "l": make_texstudio_color_command(keymap, "Plum"),
        "g": make_texstudio_color_command(keymap, "PineGreen")
    })
    pk_tex.add("g", {
        "r": make_texstudio_color_command(keymap, "Gray")
    })
    add_git_commit_sequence(keymap, pk_tex)
    pk_tex.add("b", {
        "l": make_texstudio_color_command(keymap, "Black")
    })
    pk_tex.finalize()

    keymap_texstudio["U2-C"] = make_texstudio_bracket_clipboard_command(keymap, "C-A-OpenBracket", "C-C")
    keymap_texstudio["U2-D"] = make_texstudio_bracket_clipboard_command(keymap, "C-A-CloseBracket", "C-C")
    keymap_texstudio["U2-X"] = make_texstudio_bracket_clipboard_command(keymap, "C-A-OpenBracket", "C-X")
    keymap_texstudio["U2-S"] = make_texstudio_bracket_clipboard_command(keymap, "C-A-CloseBracket", "C-X")
    keymap_texstudio["U2-V"] = make_texstudio_bracket_paste_command(keymap, "C-A-OpenBracket")
    keymap_texstudio["U2-F"] = make_texstudio_bracket_paste_command(keymap, "C-A-CloseBracket")
