import tcod

from random import randint

from game_messages import Message


class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner
        if fov_map.fov[monster.pos.y][monster.pos.x]:
            if monster.pos.distance_to(target.pos) >= 2:
                monster.pos.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                monster.fighter.attack(target)
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
        return results


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.pos.x + randint(0, 2) - 1
            random_y = self.owner.pos.y + randint(0, 2) - 1

            if random_x != self.owner.pos.x and random_y != self.owner.pos.y:
                self.owner.pos.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message(
                'The {0} is no longer confused!'.format(self.owner.name), tcod.red)})

        return results
