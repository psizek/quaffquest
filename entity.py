import math
import tcod
import numpy as np

from render_fns import RenderOrder

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        
        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
        """Move the entity by a given amount"""
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
                self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        dungeon = np.empty((game_map.width, game_map.height), dtype=np.int8)
        for x in range(game_map.width):
            for y in range(game_map.height):
                dungeon[x,y] = (0 if game_map.tiles[x][y].blocked else 1)

        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                dungeon[entity.x, entity.y] = 0

        astar = tcod.path.AStar(dungeon) #defaults diagonal to 1.41

        path = astar.get_path(self.x, self.y, target.x, target.y)

        if len(path) > 0 and len(path) < 25:
            x, y = path[0]
            if x or y:
                self.x = x
                self.y = y

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.x == destination_x and entity.y == destination_y and entity.blocks:
            return entity
    return None
