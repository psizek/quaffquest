
class ItemBase:
    use_function=None
    targeting=None
    targeting_message=None
    function_kwargs=None
    def __init__(self, number=1):
        self.number = number

def item_factory(type_name, use_function, targeting, targeting_message, **kwargs):
    return type(type_name, ItemBase, dict(use_function=use_function, targeting=targeting, targeting_message=targeting_message, function_kwargs=kwargs))

#use the item_factory to generate the class, which means we can load the classes into objects at the start
#rather than generating objects with the same attributes over and over - this saves memory
#and objects get smaller necessarily as a result.

#we can even now build json and load items from there. But this should be done at the top of the engine call
#and also tracked there in some capacity.

#obselete
class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, stack=1, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
        self.number = stack
        pass
