#Requires AutoHotkey v2.0

KH_InitSnippetSequencesExt() {
    KH_PowerKey_Add(
        "g",
        "c-p",
        KH_MakePasteTextCommand("git commit 一下本 session 所在 dir 的 repo 的当前版本，并同步到远程。"),
        "__global__",
        "",
        "git commit prompt"
    )
    KH_PowerKey_Add(
        "g",
        "p-p",
        KH_MakePasteTextCommand("pull 到本地，然后合并冲突，然后 push 到远程。"),
        "__global__",
        "",
        "pull merge push prompt"
    )
    KH_PowerKey_Add(
        "g",
        "l-c",
        KH_MakePasteTextCommand(
            "上一个 commit 至今的效果并不好。让本地和远程均把 HEAD 退回上一个 git commit，并把上一个 git commit 至今的改动分支出去。"
        ),
        "__global__",
        "",
        "rollback branch prompt"
    )
}
