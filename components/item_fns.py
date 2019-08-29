import tcod
from game_messages import Message
from components.ai import ConfusedMonster


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message(
            'You are already at full health', tcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message(
            'Your wounds start to feel better!', tcod.green)})

    return results


def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map: tcod.map.Map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range: int = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and fov_map.fov[entity.y][entity.x]:
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message(
            'A lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message(
            'No enemy is close enough to strike.', tcod.red)})

    return results


def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map: tcod.map.Map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x: int = kwargs.get('target_x')
    target_y: int = kwargs.get('target_y')

    results = []

    if not fov_map.fov[target_y][target_x]:
        results.append({'consumed': False, 'message': Message(
            'You cannot target a tile outside your field of view.', tcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message(
        'The fireball explodes, burning everything within {0} tiles!'.format(radius), tcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message(
                'The {0} gets burned for {1} hit points.'.format(entity.name, damage), tcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x: int = kwargs.get('target_x')
    target_y: int = kwargs.get('target_y')

    results = []

    if not fov_map.fov[target_y][target_x]:
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} look vacant, as he starts to stumble around!'.format(entity.name), tcod.light_green)})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', tcod.yellow)})

    return results