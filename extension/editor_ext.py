from keyhac import *

def init_editor_ext(keymap):
    # Edit boxes
    keymap_edit = keymap.defineWindowKeymap( class_name="Edit" )
    keymap_edit[ "C-D" ] = "Delete"
    keymap_edit[ "C-H" ] = "Back"

    # Notepad specific
    keymap_notepad = keymap.defineWindowKeymap( exe_name="notepad.exe", class_name="Edit" )
    keymap_notepad[ "C-X" ] = keymap.defineMultiStrokeKeymap("C-X")
    keymap_notepad[ "C-P" ] = "Up"
    keymap_notepad[ "C-N" ] = "Down"
    keymap_notepad[ "C-F" ] = "Right"
    keymap_notepad[ "C-B" ] = "Left"
    keymap_notepad[ "C-A" ] = "Home"
    keymap_notepad[ "C-E" ] = "End"
    keymap_notepad[ "C-X" ][ "C-S" ] = "C-S"
    keymap_notepad[ "C-Y" ] = "C-V"
