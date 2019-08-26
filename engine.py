import tcod
import tcod.event
import tcod.map

from render_fns import clear_all, render_all, RenderOrder
from state import State

from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from map_objects.game_map import GameMap
from fov_fns import initialize_fov
from game_messages import MessageLog
from game_states import GameStates

def main():
    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

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
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)

    entities = [player]

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    with tcod.console_init_root(screen_width, screen_height, 'Quaff Quest', False, tcod.RENDERER_SDL2) as root_con:

        con = tcod.console.Console(screen_width, screen_height)
        panel = tcod.console.Console(screen_width, panel_height)

        state = State()

        game_map = GameMap(map_width, map_height)
        game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

        fov_recompute = True
        fov_map = initialize_fov(game_map)

        message_log = MessageLog(message_x, message_width, message_height)

        game_state = GameStates.PLAYERS_TURN

        #game loop
        while True:
            for event in tcod.event.wait():
                state.action = None
                state.dispatch(event)

                if fov_recompute:
                    fov_map.compute_fov(player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

                render_all(root_con, con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, bar_width, panel_y, state.mouse_pos, colors)
                fov_recompute = False
                tcod.console_flush()
                clear_all(root_con, con, entities)

                if state.action:

                    move = state.action.get('move')
                    exit = state.action.get('exit')
                    fullscreen = state.action.get('fullscreen')

                    player_turn_results = []

                    if exit:
                        return True

                    if fullscreen:
                        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

                    if move and game_state == GameStates.PLAYERS_TURN:
                        dx, dy = move
                        destination_x = player.x + dx
                        destination_y = player.y + dy
                        if not game_map.is_blocked(destination_x, destination_y):
                            target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                            if target:
                                player.fighter.attack(target)
                                attack_results = player.fighter.attack(target)
                                player_turn_results.extend(attack_results)
                            else:
                                player.move(dx, dy)
                                fov_recompute = True
                            game_state = GameStates.ENEMY_TURN
                    for player_turn_result in player_turn_results:
                        message = player_turn_result.get('message')
                        dead_entity = player_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)
                            message_log.add_message(message)

                    if game_state == GameStates.ENEMY_TURN:
                        for entity in entities:
                            if entity.ai:
                                enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
                                
                                for enemy_turn_result in enemy_turn_results:
                                    message = enemy_turn_result.get('message')
                                    dead_entity = enemy_turn_result.get('dead')
                                    if message:
                                        message_log.add_message(message)
                                    if dead_entity:
                                        if dead_entity == player:
                                            message, game_state = kill_player(dead_entity)
                                        else:
                                            message = kill_monster(dead_entity)
                                        message_log.add_message(message)
                                        if game_state == GameStates.PLAYER_DEAD:
                                            break
                                if game_state == GameStates.PLAYER_DEAD:
                                        break
                        else:
                            game_state = GameStates.PLAYERS_TURN


#https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185
#this tidbit is actually pretty cool. kudos to the guy who wrote that.
if __name__ == '__main__':
    main()
