import tcod as libtcod

def render_all(root_con, con, entities, screen_width, screen_height):
    """Draw all entities in the list"""
    for entity in entities:
        draw_entity(root_con, con, entity)
    con.blit(root_con, 0, 0, 0, 0, screen_width, screen_height)

def clear_all(root_con, con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(root_con, con, entity):
    con.default_fg = entity.color
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    """erase character representing object"""
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
