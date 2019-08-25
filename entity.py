class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        """Move the entity by a given amount"""
        self.x += dx
        self.y += dy

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.x == destination_x and entity.y == destination_y and entity.blocks:
            return entity
    return None
