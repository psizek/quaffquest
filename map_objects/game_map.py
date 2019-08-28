from random import randint
from typing import List

import tcod

from render_fns import RenderOrder

from map_objects.rectangle import Rect
from map_objects.tile import Tile
from entity import Entity
from components.fighter import Fighter
from components.ai import BasicMonster 
from components.item import Item

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms: int, room_min_size: int, room_max_size: int, map_width: int, map_height: int, player, entities, max_monsters_per_room: int, max_items_per_room: int):
        rooms: List[Rect] = []
        num_rooms: int = 0

        for r in range(max_rooms):
            w: int = randint(room_min_size, room_max_size)
            h: int = randint(room_min_size, room_max_size)
            x: int = randint(0, map_width - w - 1)
            y: int = randint(0, map_height - h - 1)

            new_room: Rect = Rect(x, y, w, h)

            #for-else loop
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room: Rect):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1: int, x2: int, y: int):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1: int, y2: int, x: int):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room: Rect, entities, max_monsters_per_room: int, max_items_per_room: int):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x: int = randint(room.x1 + 1, room.x2 - 1)
            y: int = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                entities.append(monster)
        
        for i in range(number_of_items):
            x: int = randint(room.x1 + 1, room.x2 - 1)
            y: int = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item = Entity(x, y, '!', tcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, item=Item())
                entities.append(item)

    def is_blocked(self, x: int, y: int):
        return (self.tiles[x][y].blocked)
