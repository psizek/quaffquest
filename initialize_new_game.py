import constants as c

import tcod

from components.fighter import Fighter
from components.inventory import Inventory
from entity import Entity
from map_objects.game_map import GameMap
from render_fns import RenderOrder
from game_messages import MessageLog
from game_states import GameStates


def get_game_variables():
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    entities = [player]

    game_map = GameMap(c.MAP_WIDTH, c.MAP_HEIGHT)
    game_map.make_map(c.MAX_ROOMS, c.ROOM_MIN_SIZE, c.ROOM_MAX_SIZE,
                      c.MAP_WIDTH, c.MAP_HEIGHT, player, entities,
                      c.MAX_MONSTERS_PER_ROOM, c.MAX_ITEMS_PER_ROOM)

    message_log = MessageLog(c.MESSAGE_X, c.MESSAGE_WIDTH, c.MESSAGE_HEIGHT)

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state