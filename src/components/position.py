from __future__ import annotations
import tcod.path
import math
import numpy as np

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Move the entity by a given amount"""
        self.x += dx
        self.y += dy

    def move_towards(self, target_x: int, target_y: int, game_map, entities):
        """Move entity towards target"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        """Move entity towards target with astar"""
        dungeon = np.empty((game_map.width, game_map.height), dtype=np.int8)
        for x in range(game_map.width):
            for y in range(game_map.height):
                dungeon[x, y] = (0 if game_map.tiles[x][y].blocked else 1)

        for entity in entities:
            if entity.blocks and entity.pos != self and entity != target:
                dungeon[entity.pos.x, entity.pos.y] = 0

        astar = tcod.path.AStar(dungeon)  # defaults diagonal to 1.41

        path = astar.get_path(self.x, self.y, target.pos.x, target.pos.y)

        if len(path) > 0 and len(path) < 25:
            x, y = path[0]
            if x or y:
                self.x = x
                self.y = y
    
    @staticmethod
    def distance_static(a, b, x, y):
        return math.sqrt((x - a)**2 + (y - b)**2)

    def distance(self, x, y) -> float:
        return Position.distance_static(self.x, self.y, x, y)

    def distance_to(self, other: Position) -> float:
        return self.distance(other.x, other.y)