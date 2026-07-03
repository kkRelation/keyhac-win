from keyhac import *

def init_mouse_ext(keymap, keymap_global):
    scroll_steps = {
        "": 1.0,
        "S-": 1.0,
        "C-": 5.0,
        "C-S-": 20.0,
    }

    keymap_global[ "U0-A-Left"  ] = keymap.MouseMoveCommand(-10,0)
    keymap_global[ "U0-A-Right" ] = keymap.MouseMoveCommand(10,0)
    keymap_global[ "U0-A-Up"    ] = keymap.MouseMoveCommand(0,-10)
    keymap_global[ "U0-A-Down"  ] = keymap.MouseMoveCommand(0,10)
    keymap_global[ "D-U0-A-Space" ] = keymap.MouseButtonDownCommand('left')
    keymap_global[ "U-U0-A-Space" ] = keymap.MouseButtonUpCommand('left')
    keymap_global[ "U0-A-PageUp" ] = keymap.MouseWheelCommand(1.0)
    keymap_global[ "U0-A-PageDown" ] = keymap.MouseWheelCommand(-1.0)

    for modifier, step in scroll_steps.items():
        keymap_global[f"{modifier}U0-H"] = keymap.MouseHorizontalWheelCommand(-step)
        keymap_global[f"{modifier}U0-J"] = keymap.MouseWheelCommand(-step)
        keymap_global[f"{modifier}U0-K"] = keymap.MouseWheelCommand(step)
        keymap_global[f"{modifier}U0-L"] = keymap.MouseHorizontalWheelCommand(step)
