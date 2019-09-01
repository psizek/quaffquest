import tcod

from game_messages import Message
from game_states import GameStates
from render_order import RenderOrder


def kill_player(player):
    player.render.char = '%'
    player.render.color = tcod.dark_red

    return Message('You died!', tcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message(
        f'{monster.name.capitalize()} is dead!', tcod.orange)

    monster.render.char = '%'
    monster.render.color = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = f'remains of {monster.name}'
    monster.render.render_order = RenderOrder.CORPSE

    return death_message
