import tcod

from enum import Enum, auto
from game_states import GameStates
from menu import inventory_menu, level_up_menu, character_screen


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse_pos, entities, fov_map):
    names = [entity.name for entity in entities if entity.x ==
             mouse_pos.x and entity.y == mouse_pos.y and fov_map.fov[entity.y, entity.x] == True]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel: tcod.console.Console, x: int, y: int, total_width: int, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    panel.draw_rect(x, y, total_width, 1, 0, None, back_color)

    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, 0, None, bar_color)

    panel.print(int(x + total_width/2), y,
                '{0}: {1}/{2}'.format(name, value, maximum), tcod.white, None, 1, tcod.CENTER)


def render_all(root_con: tcod.console.Console, con: tcod.console.Console, panel: tcod.console.Console, entities, player, game_map, fov_map, fov_recompute: bool, message_log, bar_width, panel_y: int, mouse_pos, colors, game_state: GameStates):
    """Render characters on the console screen"""
    render_main_map(con, entities, player, game_map,
                    fov_map, fov_recompute, colors)
    con.blit(root_con)
    render_panel(panel, message_log, bar_width,
                 player, mouse_pos, entities, fov_map, game_map.dungeon_level)
    panel.blit(root_con, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
        inventory_menu(root_con, inventory_title, player, 50)
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(
            root_con, 'Level up! Choose a stat to raise:', player, 40)
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(root_con, player, 30, 10)


def render_main_map(con, entities, player, game_map, fov_map, fov_recompute, colors):
    # render tiles
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible: bool = fov_map.fov[y][x]
                wall: bool = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        tcod.console_set_char_background(
                            con, x, y, colors.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(
                            con, x, y, colors.get('light_ground'), tcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(
                            con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(
                            con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)
    entities_in_render_order = sorted(
        entities, key=lambda x: x.render_order.value)

    # render entities
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)


def render_panel(panel, message_log, bar_width, player, mouse_pos, entities, fov_map, dungeon_level: int):
    panel.default_bg = tcod.black
    panel.clear()

    y: int = 1
    for message in message_log.messages:
        panel.print(message_log.x, y, message.text, message.color)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp,
               player.fighter.max_hp, tcod.light_red, tcod.darker_red)
    panel.print(1, 3, f'Dungeon Level: {dungeon_level}')

    panel.print(1, 0, get_names_under_mouse(
        mouse_pos, entities, fov_map), tcod.light_gray)


def clear_all(con: tcod.console.Console, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con: tcod.console.Console, entity, fov_map, game_map):
    if fov_map.fov[entity.y][entity.x] or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        con.default_fg = entity.color
        tcod.console_put_char(con, entity.x, entity.y,
                              entity.char, tcod.BKGND_NONE)


def clear_entity(con: tcod.console.Console, entity):
    """erase character representing object"""
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
