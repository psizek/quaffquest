import shelve

from pathlib import Path


def save_game(player, entities, game_map, message_log, game_state):
    root_path = Path(__file__).parent.parent
    path = root_path / 'savegame.dat'
    with shelve.open(str(path), 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state


def load_game():
    root_path = Path(__file__).parent.parent
    path = root_path / 'savegame.dat'
    if not path.is_file():
        raise FileNotFoundError

    with shelve.open(str(path), 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state
