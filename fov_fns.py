import tcod.map


def initialize_fov(game_map):
    fov_map = tcod.map.Map(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            fov_map.transparent[y][x] = not game_map.tiles[x][y].block_sight
            fov_map.walkable[y][x] = not game_map.tiles[x][y].blocked

    return fov_map
