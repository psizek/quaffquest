import tcod

def menu(root_con, header, options, width):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    header_height = root_con.get_height_rect(0, 0, width, root_con.height, header)
    height = len(options) + header_height

    window = tcod.console.Console(width, height)

    window.print_box(0, 0, width, height, header, tcod.white)
    
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        window.print(0, y, text, tcod.white)
        y += 1
        letter_index += 1

    x = int((root_con.width - width) / 2)
    y = int((root_con.height - height) /2)
    window.blit(root_con, x, y, 0, 0, width, height, 1.0, 0.7)

def inventory_menu(root_con, header, inventory, inventory_width):
    """show a menu with each item of the inventory as an option"""
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory.items]

    menu(root_con, header, options, inventory_width)
