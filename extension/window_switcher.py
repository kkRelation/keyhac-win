from keyhac import *
import pyauto

from .list_window_ext import schedule_list_window_search


def init_window_switcher(keymap, keymap_global):
    def command_PopWindowList():
        if keymap.isListWindowOpened():
            keymap.cancelListWindow()
            return

        def popWindowList():
            window_list = []
            root = pyauto.Window.getDesktop()
            wnd = root.getFirstChild()

            def activate(wnd):
                def _activate():
                    if wnd.isMinimized():
                        wnd.restore()
                    wnd.getLastActivePopup().setForeground()

                return _activate

            while wnd:
                if wnd.isVisible() and wnd.getText() and wnd.getClassName() != "Shell_TrayWnd":
                    exe_name = wnd.getProcessName().lower()
                    if exe_name.endswith(".exe"):
                        exe_name = exe_name[:-4]
                    display_text = "%-15s | %s" % (exe_name, wnd.getText())
                    window_list.append((display_text, activate(wnd)))
                wnd = wnd.getNext()

            listers = [("Windows", cblister_FixedPhrase(window_list))]

            item, mod = keymap.popListWindow(listers)
            if item:
                item[1]()

        keymap.delayedCall(popWindowList, 0)
        schedule_list_window_search(keymap)

    keymap_global["U0-W"] = command_PopWindowList

    # Smart Enter logic
    keymap_listwindow = keymap.defineWindowKeymap(exe_name="keyhac.exe", class_name="KeyhacListWindow")

    def command_SmartEnter():
        keymap.InputKeyCommand("Enter")()

        def checkAndRetry():
            if keymap.isListWindowOpened():
                keymap.InputKeyCommand("Enter")()

        keymap.delayedCall(checkAndRetry, 100)

    keymap_listwindow["Enter"] = command_SmartEnter
