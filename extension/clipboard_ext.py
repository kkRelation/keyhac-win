import os
import datetime
from keyhac import *
from .clipboard_commands import make_copy_selection_before_passthrough_command

def init_clipboard_ext(keymap, keymap_global=None):
    keymap.clipboard_history.enableHook(True)
    keymap.clipboard_history.maxnum = 1000
    keymap.clipboard_history.quota = 10*1024*1024

    fixed_items = [
        ( "name@server.net",     "name@server.net" ),
        ( "Address",             "San Francisco, CA 94128" ),
        ( "Phone number",        "03-4567-8901" ),
    ]

    def dateAndTime(fmt):
        def _dateAndTime():
            return datetime.datetime.now().strftime(fmt)
        return _dateAndTime

    datetime_items = [
        ( "YYYY/MM/DD HH:MM:SS",   dateAndTime("%Y/%m/%d %H:%M:%S") ),
        ( "YYYYMMDD_HHMMSS",       dateAndTime("%Y%m%d_%H%M%S") ),
    ]

    def quoteClipboardText():
        s = getClipboardText()
        if not s: return ""
        return "".join([keymap.quote_mark + line for line in s.splitlines(True)])

    def toHalfWidthClipboardText():
        s = getClipboardText()
        if not s: return ""
        full_width_chars = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！”＃＄％＆’（）＊＋，−．／：；＜＝＞？＠［￥］＾＿‘｛｜｝～０１２３４５６７８９　"
        half_width_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}～0123456789 "
        return s.translate(str.maketrans(full_width_chars,half_width_chars))

    def command_SaveClipboardToDesktop():
        text = getClipboardText()
        if not text: return
        fullpath = os.path.join( getDesktopPath(), datetime.datetime.now().strftime("clip_%Y%m%d_%H%M%S.txt") )
        with open( fullpath, "wb" ) as fd:
            fd.write(b"\xEF\xBB\xBF" + text.replace("\r\n","\n").replace("\n","\r\n").encode("utf-8"))
        keymap.editTextFile(fullpath)

    other_items = [
        ( "Quote clipboard",            quoteClipboardText ),
        ( "To Half-Width",              toHalfWidthClipboardText ),
        ( "Save clipboard to Desktop",  command_SaveClipboardToDesktop ),
    ]

    keymap.cblisters += [
        ( "Fixed phrase", cblister_FixedPhrase(fixed_items) ),
        ( "Date-time", cblister_FixedPhrase(datetime_items) ),
        ( "Others", cblister_FixedPhrase(other_items) ),
    ]

    if keymap_global is not None:
        cmd = make_copy_selection_before_passthrough_command(keymap, "A-L")
        keymap_global["U0-A"] = cmd
