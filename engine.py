from typing import List, Dict, Any

import tcod
import tcod.event
import tcod.map

import constants as c
from initialize_new_game import get_game_variables

from render_fns import clear_all, render_all
from state import Event_State_Manager, MainMenu_State

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_fns import initialize_fov
from game_messages import Message
from game_states import GameStates

from data_loaders import load_game, save_game
from menu import main_menu, message_box


def main():

    tcod.console_set_custom_font(
        'arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    with tcod.console_init_root(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.WINDOW_TITLE, False, tcod.RENDERER_SDL2) as root_con:

        con: tcod.console.Console = tcod.console.Console(
            c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        panel: tcod.console.Console = tcod.console.Console(
            c.SCREEN_WIDTH, c.PANEL_HEIGHT)

        player = None
        entities = []
        game_map = None
        message_log = None
        game_state = None

        show_main_menu: bool = True
        show_load_error_message: bool = False

        main_menu_img_background = tcod.image_load('menu_background.png')

        state = MainMenu_State()

        while True:
            for event in tcod.event.wait():
                state.dispatch(event)

                if show_main_menu:
                    main_menu(root_con, main_menu_img_background)

                    if show_load_error_message:
                        message_box(root_con, 'No save game to load', 50)

                    tcod.console_flush()

                    if state.action:
                        new_game = state.action.get('new_game')
                        load_saved_game = state.action.get('load_game')
                        exit_game = state.action.get('exit')

                        if show_load_error_message and (new_game or load_saved_game or exit_game):
                            show_load_error_message = False
                        elif new_game:
                            player, entities, game_map, message_log, game_state = get_game_variables()
                            game_state = GameStates.PLAYERS_TURN
                            show_main_menu = False
                        elif load_saved_game:
                            try:
                                player, entities, game_map, message_log, game_state = load_game()
                                show_main_menu = False
                            except FileNotFoundError:
                                show_load_error_message = True
                        elif exit_game:
                            return
                else:
                    root_con.clear()
                    play_game(player, entities, game_map, message_log,
                              game_state, root_con, con, panel)

                    return
                    #show_main_menu = True


def play_game(player, entities, game_map, message_log, game_state, root_con, con, panel):
    fov_recompute: bool = True
    fov_map: tcod.map.Map = initialize_fov(game_map)

    previous_game_state = game_state

    targeting_item = None

    state = Event_State_Manager()

    # game loop
    while True:
        for event in tcod.event.wait():
            state.run_state(game_state, event)

            if fov_recompute:
                fov_map.compute_fov(
                    player.x, player.y, c.FOV_RADIUS, c.FOV_LIGHT_WALLS, c.FOV_ALGORITHM)

            render_all(root_con, con, panel, entities, player, game_map, fov_map, fov_recompute,
                       message_log, c.BAR_WIDTH, c.PANEL_Y, state.mouse_pos, c.COLORS, game_state)
            fov_recompute = False
            tcod.console_flush()
            clear_all(con, entities)

            if state.action:

                move = state.action.get('move')
                rest = state.action.get('rest')
                pickup = state.action.get('pickup')
                show_inventory = state.action.get('show_inventory')
                drop_inventory = state.action.get('drop_inventory')
                inventory_index = state.action.get('inventory_index')
                take_stairs = state.action.get('take_stairs')
                level_up = state.action.get('level_up')
                show_character_screen = state.action.get('show_character_screen')
                exit = state.action.get('exit')
                fullscreen = state.action.get('fullscreen')
                target_pt = state.action.get('target')

                player_turn_results: List[Dict[str, Any]] = []

                if exit:
                    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                        game_state = previous_game_state
                    elif game_state == GameStates.TARGETING:
                        player_turn_results.append(
                            {'targeting_cancelled': True})
                    else:
                        save_game(player, entities, game_map,
                                  message_log, game_state)
                        return

                if fullscreen:
                    tcod.console_set_fullscreen(
                        not tcod.console_is_fullscreen())

                if move and game_state == GameStates.PLAYERS_TURN:
                    dx, dy = move
                    destination_x = player.x + dx
                    destination_y = player.y + dy
                    if not game_map.is_blocked(destination_x, destination_y):
                        target = get_blocking_entities_at_location(
                            entities, destination_x, destination_y)

                        if target:
                            player.fighter.attack(target)
                            attack_results = player.fighter.attack(target)
                            player_turn_results.extend(attack_results)
                        else:
                            player.move(dx, dy)
                            fov_recompute = True
                        game_state = GameStates.ENEMY_TURN
                elif pickup and game_state == GameStates.PLAYERS_TURN:
                    for entity in entities:
                        if entity.item and entity.x == player.x and entity.y == player.y:
                            pickup_results = player.inventory.add_item(
                                entity)
                            player_turn_results.extend(pickup_results)
                            break
                    else:
                        message_log.add_message(
                            Message('There is nothing here to pick up.', tcod.yellow))
                elif rest and game_state == GameStates.PLAYERS_TURN:
                    game_state = GameStates.ENEMY_TURN

                if show_inventory:
                    previous_game_state = game_state
                    game_state = GameStates.SHOW_INVENTORY
                if drop_inventory:
                    previous_game_state = game_state
                    game_state = GameStates.DROP_INVENTORY

                if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
                    item = player.inventory.items[inventory_index]
                    if game_state == GameStates.SHOW_INVENTORY:
                        player_turn_results.extend(player.inventory.use(
                            item, entities=entities, fov_map=fov_map))
                    elif game_state == GameStates.DROP_INVENTORY:
                        player_turn_results.extend(
                            player.inventory.drop_item(item))

                if take_stairs and game_state == GameStates.PLAYERS_TURN:
                    for entity in entities:
                        if entity.stairs and entity.x == player.x and entity.y == player.y:
                            entities = game_map.next_floor(
                                player, message_log, c)
                            fov_map = initialize_fov(game_map)
                            fov_recompute = True
                            tcod.console_clear(con)
                            break
                    else:
                        message_log.add_message(
                            Message('There are no stairs here.', tcod.yellow))
                
                if level_up:
                    if level_up == 'hp':
                        player.fighter.max_hp += 20
                        player.fighter.hp += 20
                    elif level_up == 'str':
                        player.fighter.power += 1
                    elif level_up == 'def':
                        player.fighter.defense += 1
                    game_state = previous_game_state
                if show_character_screen:
                    previous_game_state = game_state
                    game_state = GameStates.CHARACTER_SCREEN


                if game_state == GameStates.TARGETING:
                    if target_pt:
                        target_x, target_y = target_pt
                        item_use_results = player.inventory.use(
                            targeting_item, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
                        player_turn_results.extend(item_use_results)

                for player_turn_result in player_turn_results:
                    message = player_turn_result.get('message')
                    dead_entity = player_turn_result.get('dead')
                    item_added = player_turn_result.get('item_added')
                    item_consumed = player_turn_result.get('consumed')
                    item_dropped = player_turn_result.get('item_dropped')
                    targeting = player_turn_result.get('targeting')
                    targeting_cancelled = player_turn_result.get(
                        'targeting_cancelled')
                    xp = player_turn_result.get('xp')

                    if message:
                        message_log.add_message(message)
                    if targeting_cancelled:
                        game_state = previous_game_state
                        message_log.add_message(
                            Message('Targeting cancelled'))
                    if xp:
                        leveled_up = player.level.add_xp(xp)
                        message_log.add_message(
                            Message('You gain {0} experience points.'.format(xp)))
                        if leveled_up:
                            message_log.add_message(Message(
                                'Your battle skills grow stronger! You reached level {0}'.format(
                                    player.level.current_level) + '!', tcod.yellow))
                            previous_game_state = game_state
                            game_state = GameStates.LEVEL_UP
                    if dead_entity:
                        if dead_entity == player:
                            message, game_state = kill_player(dead_entity)
                        else:
                            message = kill_monster(dead_entity)
                        message_log.add_message(message)
                    if item_added:
                        entities.remove(item_added)
                        game_state = GameStates.ENEMY_TURN
                    if item_consumed:
                        game_state = GameStates.ENEMY_TURN
                    if targeting:
                        previous_game_state = GameStates.PLAYERS_TURN
                        game_state = GameStates.TARGETING
                        targeting_item = targeting
                        message_log.add_message(
                            targeting_item.item.targeting_message)
                    if item_dropped:
                        entities.append(item_dropped)

                        game_state = GameStates.ENEMY_TURN

                if game_state == GameStates.ENEMY_TURN:
                    for entity in entities:
                        if entity.ai:
                            enemy_turn_results = entity.ai.take_turn(
                                player, fov_map, game_map, entities)

                            for enemy_turn_result in enemy_turn_results:
                                message = enemy_turn_result.get('message')
                                dead_entity = enemy_turn_result.get('dead')
                                if message:
                                    message_log.add_message(message)
                                if dead_entity:
                                    if dead_entity == player:
                                        message, game_state = kill_player(
                                            dead_entity)
                                    else:
                                        message = kill_monster(dead_entity)
                                    message_log.add_message(message)
                                    if game_state == GameStates.PLAYER_DEAD:
                                        break
                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    else:
                        game_state = GameStates.PLAYERS_TURN


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do/419185#419185
# this tidbit is actually pretty cool. kudos to the guy who wrote that.
if __name__ == '__main__':
    main()
