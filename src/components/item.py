from pathlib import Path
import json

from game_messages import Message
from components.item_fns import heal, cast_confuse, cast_lightning, cast_fireball


class ItemBase:
    """base for item component class"""
    use_function = None
    targeting = None
    targeting_message = None
    function_kwargs = None

    def __init__(self, number=1):
        self.number = number


def item_factory(type_name, use_function, targeting, targeting_message, kwargs):
    """returns an item component class"""
    return type(type_name, (ItemBase,), dict(use_function=staticmethod(use_function), targeting=targeting, targeting_message=targeting_message, function_kwargs=kwargs))


def get_item_classes():
    """loads item component classes from file"""
    root_path = Path(__file__).parent.parent.parent
    path = root_path / 'data' / 'json' / 'items.json'
    with path.open() as f:
        item_objs = json.load(f)
        item_classes = {}
        for item in item_objs:
            if 'targeting_message' in item:
                message = Message(
                    item['targeting_message']['text'], item['targeting_message']['color'])
            else:
                message = None
            item_classes[item['classname']] = item_factory(item['classname'], globals(
            )[item['use_function']], item['targeting'], message, item['function_kwargs'])
        return item_classes


# deprecated: don't use this going forward
class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, stack=1, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
        self.number = stack
        pass
