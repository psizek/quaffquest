from render_order import RenderOrder
from components.item import Item
from components.render import RenderData
from components.position import Position


class Entity:
    """ A generic object to represent players, enemies, items, etc. """

    def __init__(self, x: int, y: int, char, color, name, blocks: bool = False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, item=None, inventory=None, stairs=None, level=None, equipment=None, equippable=None):
        self.pos = Position(x, y)
        self.render = RenderData(char, color, render_order)
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equippable = equippable
        self.equipment = equipment

        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self
        if self.item:
            self.item.owner = self
        if self.inventory:
            self.inventory.owner = self
        if self.stairs:
            self.stairs.owner = self
        if self.level:
            self.level.owner = self
        if self.equipment:
            self.equipment.owner = self
        if self.equippable:
            self.equippable.owner = self
            if not self.item:
                self.item = Item()
                self.item.owner = self

def get_blocking_entities_at_location(entities, destination_x: int, destination_y: int):
    for entity in entities:
        if entity.pos.x == destination_x and entity.pos.y == destination_y and entity.blocks:
            return entity
    return None
