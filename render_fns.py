import tcod

from enum import Enum

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    panel.draw_rect(x, y, total_width, 1, 0, None, back_color)

    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, 0, None, bar_color)

    panel.default_fg = tcod.white
    panel.print(int(x + total_width/2), y, '{0}: {1}/{2}'.format(name, value, maximum), None, None, 1, tcod.CENTER)

def render_all(root_con, con, panel, entities, player, game_map, fov_map, fov_recompute, bar_width, panel_y, colors):
    """Render characters on the console screen"""
    #render tiles
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = fov_map.fov[y][x]
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colors.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colors.get('light_ground'), tcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    #render entities
    for entity in entities_in_render_order:
        draw_entity(root_con, con, entity, fov_map)

    con.blit(root_con)

    panel.default_bg = tcod.black
    panel.clear()
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, tcod.light_red, tcod.darker_red)

    panel.blit(root_con, 0, panel_y)

def clear_all(root_con, con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(root_con, con, entity, fov_map):
    if fov_map.fov[entity.y][entity.x]:
        con.default_fg = entity.color
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity):
    """erase character representing object"""
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
