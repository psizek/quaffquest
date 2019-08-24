import tcod
import tcod.event

from input_handlers import handle_keys
from render_fns import clear_all, render_all

from entity import Entity
from map_objects.game_map import GameMap

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    colors = {
            'dark_wall': tcod.Color(0, 0, 100),
            'dark_ground': tcod.Color(50, 50, 150)
            }

    player = Entity(int(screen_width/2), int(screen_height/2), '@', tcod.white)

    entities = [player]

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    with tcod.console_init_root(screen_width, screen_height, 'Quaff Quest', False, tcod.RENDERER_SDL2) as root_con:

        con = tcod.console.Console(screen_width, screen_height)

        game_map = GameMap(map_width, map_height)
        game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

        #game loop
        while True:
            for event in tcod.event.wait():
                action = None
                if event.type == 'QUIT':
                    raise SystemExit()
                if event.type == 'KEYDOWN':
                    action = handle_keys(event)

                render_all(root_con, con, entities, game_map, screen_width, screen_height, colors)
                tcod.console_flush()
                clear_all(root_con, con, entities)

                if action:

                    move = action.get('move')
                    exit = action.get('exit')
                    fullscreen = action.get('fullscreen')

                    if exit:
                        return True

                    if fullscreen:
                        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

                    if move:
                        dx, dy = move
                        if not game_map.is_blocked(player.x + dx, player.y + dy):
                            player.move(dx, dy)

#https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185
#this is actually pretty cool. kudos to the guy who wrote that.
if __name__ == '__main__':
    main()
