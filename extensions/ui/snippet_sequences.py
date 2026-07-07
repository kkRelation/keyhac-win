from extensions.clipboard.clipboard_commands import make_paste_text_without_history_command
from extensions.input.key_inject import direct_inject_keys

ENABLE_RESUME_SEQUENCE = False
ENABLE_FORK_SEQUENCE = False


def make_home_then_paste_text_command(keymap, text):
    paste_text = make_paste_text_without_history_command(keymap, text)

    def _command():
        direct_inject_keys("Home")
        keymap.delayedCall(paste_text, 50)

    return _command


def add_git_commit_sequence(keymap, powerkey):
    powerkey.add(
        "g",
        {
            "c-p": make_paste_text_without_history_command(
                keymap, "git commit 一下本 session 所在 dir 的 repo 的当前版本，并同步到远程。"
            ),
            "p-p": make_paste_text_without_history_command(
                keymap, "pull 到本地，然后合并冲突，然后 push 到远程。"
            ),
            "l-c": make_paste_text_without_history_command(
                keymap,
                (
                    "上一个 commit 至今的效果并不好。"
                    "让本地和远程均把 HEAD 退回上一个 git commit，"
                    "并把上一个 git commit 至今的改动分支出去。"
                ),
            ),
        },
    )


def add_resume_sequence(keymap, powerkey):
    powerkey.add(
        "r",
        {
            "s-u": make_paste_text_without_history_command(
                keymap,
                "/resume",
                post_keys=["Enter"],
            ),
        },
    )


def add_fork_sequence(keymap, powerkey):
    powerkey.add(
        "f",
        {
            "r-k": make_paste_text_without_history_command(
                keymap,
                "/fork",
                post_keys=["Enter"],
            ),
        },
    )


def add_translate_prompt_sequence(keymap, powerkey):
    powerkey.add(
        "f",
        {
            "y-v": make_home_then_paste_text_command(keymap, "翻译至最简："),
        },
    )
