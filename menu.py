import tcod


def menu(root_con, header: str, options, width: int):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    header_height = root_con.get_height_rect(
        0, 0, width, root_con.height, header)
    height = len(options) + header_height

    window = tcod.console.Console(width, height)

    window.print_box(0, 0, width, height, header, tcod.white)

    y: int = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        window.print(0, y, text, tcod.white)
        y += 1
        letter_index += 1

    x: int = int((root_con.width - width) / 2)
    y = int((root_con.height - height) / 2)
    window.blit(root_con, x, y, 0, 0, width, height, 1.0, 0.7)


def inventory_menu(root_con, header: str, player, inventory_width):
    """show a menu with each item of the inventory as an option"""
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            else:
                options.append(item.name)

    menu(root_con, header, options, inventory_width)


def main_menu(root_con, background_image):
    background_image.blit_2x(root_con, 0, 0)
    root_con.print(int(root_con.width/2), int(root_con.height/2) - 4,
                   'Quaff Quest', tcod.light_yellow, None, 1, tcod.CENTER)
    root_con.print(int(root_con.width/2), int(root_con.height/2),
                   'By Phil Sizek', tcod.light_yellow, None, 1, tcod.CENTER)
    menu(root_con, '', ['Play a new game', 'Continue last game', 'Quit'], 24)


def message_box(root_con, header, width):
    menu(root_con, header, [], width)

def level_up_menu(root_con, header, player, menu_width):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.power),
               'Agility (+1 defense, from {0})'.format(player.fighter.defense)]
    menu(root_con, header, options, menu_width)


def character_screen(root_con: tcod.console.Console, player, character_screen_width: int, character_screen_height: int):
    window = tcod.console.Console(character_screen_width, character_screen_height)

    window.print_box(0, 1, window.width, window.height, 'Character Information', tcod.white)
    window.print_box(0, 2, window.width, window.height, f'Level: {player.level.current_level}', tcod.white)
    window.print_box(0, 3, window.width, window.height, f'Experience: {player.level.current_xp}', tcod.white)
    window.print_box(0, 4, window.width, window.height, f'Experience to Level: {player.level.experience_to_next_level}', tcod.white)
    window.print_box(0, 6, window.width, window.height, f'Maximum HP: {player.fighter.max_hp}', tcod.white)
    window.print_box(0, 7, window.width, window.height, f'Attack: {player.fighter.power}', tcod.white)
    window.print_box(0, 8, window.width, window.height, f'Defense: {player.fighter.defense}', tcod.white)
    x = root_con.width // 2 - character_screen_width // 2
    y = root_con.height // 2 - character_screen_height // 2
    window.blit(root_con, x, y, 0, 0, 0, 0, 1, 0.7)