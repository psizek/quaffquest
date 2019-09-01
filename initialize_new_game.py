import constants as c

import tcod

from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components.equippable import Equippable
from entity import Entity
from map_objects.game_map import GameMap
from render_order import RenderOrder
from game_messages import MessageLog
from game_states import GameStates

from equipment_slots import EquipmentSlots


def get_game_variables():
    fighter_component = Fighter(hp=100, defense=1, power=2)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component, equipment=equipment_component)
    entities = [player]

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
    dagger = Entity(0, 0, '-', tcod.sky, 'Dagger',
                    equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    game_map = GameMap(c.MAP_WIDTH, c.MAP_HEIGHT)
    game_map.make_map(c.MAX_ROOMS, c.ROOM_MIN_SIZE, c.ROOM_MAX_SIZE,
                      c.MAP_WIDTH, c.MAP_HEIGHT, player, entities)

    message_log = MessageLog(c.MESSAGE_X, c.MESSAGE_WIDTH, c.MESSAGE_HEIGHT)

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
