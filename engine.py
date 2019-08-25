import tcod
import tcod.event
import tcod.map

from render_fns import clear_all, render_all
from state import State

from components.fighter import Fighter
from entity import Entity, get_blocking_entities_at_location
from map_objects.game_map import GameMap
from fov_fns import initialize_fov
from game_states import GameStates

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
            'dark_wall': tcod.Color(0, 0, 100),
            'dark_ground': tcod.Color(50, 50, 150),
            'light_wall': tcod.Color(130, 110, 50),
            'light_ground': tcod.Color(200, 180, 50)
            }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, fighter=fighter_component)

    entities = [player]

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    with tcod.console_init_root(screen_width, screen_height, 'Quaff Quest', False, tcod.RENDERER_SDL2) as root_con:

        con = tcod.console.Console(screen_width, screen_height)
        state = State()

        game_map = GameMap(map_width, map_height)
        game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

        fov_recompute = True
        fov_map = initialize_fov(game_map)

        game_state = GameStates.PLAYERS_TURN

        #game loop
        while True:
            for event in tcod.event.wait():
                state.action = None
                state.dispatch(event)

                if fov_recompute:
                    fov_map.compute_fov(player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

                render_all(root_con, con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
                fov_recompute = False
                tcod.console_flush()
                clear_all(root_con, con, entities)

                if state.action:

                    move = state.action.get('move')
                    exit = state.action.get('exit')
                    fullscreen = state.action.get('fullscreen')

                    if exit:
                        return True

                    if fullscreen:
                        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
                    if game_state == GameStates.ENEMY_TURN:
                        for entity in entities:
                            if entity.ai:
                                entity.ai.take_turn(player, fov_map, game_map, entities)
                        game_state = GameStates.PLAYERS_TURN

                    if move and game_state == GameStates.PLAYERS_TURN:
                        dx, dy = move
                        destination_x = player.x + dx
                        destination_y = player.y + dy
                        if not game_map.is_blocked(destination_x, destination_y):
                            target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                            if target:
                                print(f'You kick the {target.name} in the shins, much to its annoyance!')
                            else:
                                player.move(dx, dy)
                                fov_recompute = True
                            game_state = GameStates.ENEMY_TURN

#https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185
#this tidbit is actually pretty cool. kudos to the guy who wrote that.
if __name__ == '__main__':
    main()
