import tcod

from input_handlers import handle_keys
from entity import Entity
from render_fns import clear_all, render_all

def main():
    screen_width = 80
    screen_height = 50

    player = Entity(int(screen_width/2), int(screen_height/2), '@', tcod.white)

    entities = [player]

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    with tcod.console_init_root(screen_width, screen_height, 'Quaff Quest', False, tcod.RENDERER_SDL2) as root_con:

        con = tcod.console.Console(screen_width, screen_height)
        #con = tcod.console_new(screen_width, screen_height) #creates console window - which console we draw to.

        key = tcod.Key()
        mouse = tcod.Mouse()

        #game loop
        while not tcod.console_is_window_closed():
            tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

            render_all(root_con, con, entities, screen_width, screen_height)
            tcod.console_flush()
            
            clear_all(root_con, con, entities)

            action = handle_keys(key)

            move = action.get('move')
            exit = action.get('exit')
            fullscreen = action.get('fullscreen')

            if exit:
                return True

            if fullscreen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

            if move:
                dx, dy = move
                player.move(dx, dy)

#https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185
#this is actually pretty cool. kudos to the guy who wrote that.
if __name__ == '__main__':
    main()
