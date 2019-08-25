import tcod

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        if fov_map.fov[monster.y][monster.x]:
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                print(f'The {monster.name} insults you! Your ego is damaged!')
