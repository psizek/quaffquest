import tcod as libtcod
from input_handlers import handle_keys

def main():
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    player_x = int(SCREEN_WIDTH/2)
    player_y = int(SCREEN_WIDTH/2)

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Quaff Quest', False)

    con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT) #creates console window - which console we draw to.

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()
        
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

#https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185
#this is actually pretty cool. kudos to the guy who wrote that.
if __name__ == '__main__':
    main()
