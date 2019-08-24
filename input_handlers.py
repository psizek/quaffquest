import tcod

def handle_keys(event: tcod.event.KeyDown):
    #movement
    key = event.sym
    if key == tcod.event.K_UP:
        return {'move': (0,-1)}
    elif key == tcod.event.K_DOWN:
        return {'move': (0, 1)}
    elif key == tcod.event.K_LEFT:
        return {'move': (-1, 0)}
    elif key == tcod.event.K_RIGHT:
        return {'move': (1, 0)}

    if key == tcod.event.K_RETURN and (event.mod & tcod.event.KMOD_LALT or event.mod & tcod.event.KMOD_RALT):
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key == tcod.event.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
