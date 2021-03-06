from random import randint
from typing import List

import tcod

from render_order import RenderOrder

from game_messages import Message

from map_objects.rectangle import Rect
from map_objects.tile import Tile
from random_utils import random_choice_from_dict, from_dungeon_level
from entity import Entity
from components.item_fns import heal, cast_lightning, cast_fireball, cast_confuse
from components.fighter import Fighter
from components.ai import BasicMonster
from components.equipment import Equipment
from components.equippable import Equippable
from components.item import Item
from components.stairs import Stairs
from components.position import Position

from components.item import get_item_classes


class GameMap:
    def __init__(self, width, height, dungeon_level: int = 1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)]
                 for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms: int, room_min_size: int, room_max_size: int, map_width: int, map_height: int, player, entities):
        rooms: List[Rect] = []
        num_rooms: int = 0

        item_components = get_item_classes()
        center_of_last_room_x: int
        center_of_last_room_y: int

        for r in range(max_rooms):
            w: int = randint(room_min_size, room_max_size)
            h: int = randint(room_min_size, room_max_size)
            x: int = randint(0, map_width - w - 1)
            y: int = randint(0, map_height - h - 1)

            new_room: Rect = Rect(x, y, w, h)

            # for-else loop
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.pos.x = new_x
                    player.pos.y = new_y
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

                    self.place_entities(new_room, entities, item_components)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1
        stairs_component = Stairs(self.dungeon_level + 1)
        pos_comp = Position(center_of_last_room_x, center_of_last_room_y)
        down_stairs = Entity('>', tcod.white,
                             'Stairs', position=pos_comp, render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

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

    def place_entities(self, room: Rect, entities, item_components):
        # Get a random number of monsters
        max_monsters_per_room = from_dungeon_level(
            [[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level(
            [[1, 1], [2, 4]], self.dungeon_level)
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }
        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x: int = randint(room.x1 + 1, room.x2 - 1)
            y: int = randint(room.y1 + 1, room.y2 - 1)
            pos_comp = Position(x, y)

            if not any([entity for entity in entities if entity.pos.x == x and entity.pos.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                if monster_choice == 'orc':
                    fighter_component = Fighter(
                        hp=20, defense=0, power=4, xp=35)
                    ai_component = BasicMonster()
                    monster = Entity('o', tcod.desaturated_green, 'Orc', blocks=True, position=pos_comp,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                elif monster_choice == 'troll':
                    fighter_component = Fighter(
                        hp=30, defense=2, power=8, xp=100)
                    ai_component = BasicMonster()
                    monster = Entity('T', tcod.darker_green, 'Troll', blocks=True, position=pos_comp,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            pos_comp = Position(x, y)

            if not any([entity for entity in entities if entity.pos.x == x and entity.pos.y == y]):
                item_choice = random_choice_from_dict(item_chances)
                if item_choice == 'healing_potion':
                    item_component = item_components['HealingPotion'](1)
                    item = Entity('!', tcod.violet, 'Healing Potion', position=pos_comp,
                                  render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'sword':
                    equippable_component = Equippable(
                        EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity('/', tcod.sky, 'Sword', position=pos_comp,
                                  equippable=equippable_component)
                elif item_choice == 'shield':
                    equippable_component = Equippable(
                        EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity('[', tcod.darker_orange, 'Shield',
                                  position=pos_comp, equippable=equippable_component)
                elif item_choice == 'fireball_scroll':
                    item_component = item_components['FireballScroll'](1)
                    item = Entity('#', tcod.red, 'Fireball Scroll', position=pos_comp,
                                  render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = item_components['ConfuseScroll'](1)
                    item = Entity('#', tcod.light_pink, 'Confusion Scroll', position=pos_comp,
                                  render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = item_components['LightningScroll'](1)
                    item = Entity('#', tcod.yellow, 'Lightning Scroll', position=pos_comp, render_order=RenderOrder.ITEM,
                                  item=item_component)
                entities.append(item)

    def is_blocked(self, x: int, y: int):
        return (self.tiles[x][y].blocked)

    def next_floor(self, player, message_log, c):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(c.MAX_ROOMS, c.ROOM_MIN_SIZE, c.ROOM_MAX_SIZE,
                      c.MAP_WIDTH, c.MAP_HEIGHT, player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message(
            'You take a moment to rest, and recover your strength.', tcod.light_violet))

        return entities
