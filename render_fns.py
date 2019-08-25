import tcod

def render_all(root_con, con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
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

    #render entities
    for entity in entities:
        draw_entity(root_con, con, entity, fov_map)
    con.blit(root_con, 0, 0, 0, 0, screen_width, screen_height)

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
