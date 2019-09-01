import tcod
from game_messages import Message

from typing import List, Dict, Any

from copy import deepcopy, copy

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def get_item_match(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return item
        return False

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', tcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name), tcod.blue)
            })
            item_match = self.get_item_match(item.name)
            if item_match:
                item_match.item.number += item.item.number
            else:
                self.items.append(item)

        return results
    
    def use(self, item_entity, **kwargs):
        results: List[Dict[str, Any]] = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable
            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append(
                    {'message': Message(f'The {item_entity.name} cannot be used', tcod.yellow)})
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(
                    self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.destroy_item(item_entity)

                results.extend(item_use_results)

        return results


    def destroy_item(self, item, number=1):
        item.item.number -= number
        if item.item.number < 1:
            self.items.remove(item)

    def remove_item(self, item, number=1):
        if item.item.number - number < 1:
            self.items.remove(item)
            return item
        else:
            item.item.number -= number
            item_removed = deepcopy(item)
            item_removed.item.number = number
            return item_removed

    def drop_item(self, item):
        results = []
        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)
        item.pos = copy(self.owner.pos)

        item_removed = self.remove_item(item)
        results.append({'item_dropped': item_removed, 'message': Message(
            f'You dropped the {item.name}', tcod.yellow)})
        return results
