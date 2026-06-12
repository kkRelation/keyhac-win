from keyhac import *

from extensions.apps.url_launcher import register_url_shortcuts
from extensions.window.list_window_ext import schedule_list_window_search


def init_app_launcher(keymap, keymap_global):
    def command_PopApplicationList():
        if keymap.isListWindowOpened():
            keymap.cancelListWindow()
            return

        def popApplicationList():
            applications = [
                ("Notepad", keymap.ShellExecuteCommand(None, "notepad.exe", "", "")),
                ("Paint", keymap.ShellExecuteCommand(None, "mspaint.exe", "", "")),
            ]
            listers = [("App", cblister_FixedPhrase(applications))]
            item, mod = keymap.popListWindow(listers)
            if item:
                item[1]()

        keymap.delayedCall(popApplicationList, 0)
        schedule_list_window_search(keymap)

    keymap_global["U0-Space"] = command_PopApplicationList

    register_url_shortcuts(
        keymap,
        [
            {
                "sequence": "y-t-l",
                "url": "http://localhost:5150/admin.html",
                "browser": "firefox",
                "private": False,
                "new_window": True,
            },
        ],
    )
