# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/22 10:59
from V1.buildpatrol import BuildPatrol
from V1.strategy.action import Action
from V1.test_hero_data import origin_hero_data
from V1.test_map_data import origin_map_data
from V1.test_monster_data import origin_monster_data


class Game(object):
    def __init__(self, hero: list, monster: list, maps):
        self.hero = hero
        self.monster = monster
        self.maps = maps

    def hero_action(self, hero, step):
        # hero = [h for h in self.hero if h.protagonist == 1][0]
        if hero.is_death():
            return {"action_type": "HERO_DIED", "steps": "英雄死亡, 当前无行动"}
        res = Action().run_action(step, hero, self.monster)
        print(f"HERO >> 行动结束返回:{res}")
        return res

    def monster_action(self, hero, step):
        # print(self.monster)
        # hero = [h for h in self.monster if h.protagonist == 1][0]
        if hero.is_death():
            return {"action_type": "HERO_DIED", "steps": "英雄死亡, 当前无行动"}
        res = Action().run_action(step, hero, self.hero)
        print(f"MONSTER >> 行动结束返回:{res}")
        return res

    def check_game_over(self):
        monster = [m for m in self.monster if not m.is_death()]
        if not monster:
            return True

        hero = [h for h in self.hero if not h.is_death()]

        if not hero:
            return True

        return False

    def get_current_alive_hero(self):
        return [h for h in self.hero if not h.is_death()] + [m for m in self.monster if not m.is_death()]

    def get_current_state(self):
        return {"hero": self.hero, "monster": self.monster, "map": self.maps}

    def start(self, heroes, enemies, maps):
        pass


if __name__ == '__main__':
    from V1.strategy.handler.constant import HERO, ENEMY_A, ENEMY_B, MAPS

    hero = HERO
    maps = MAPS
    enemies = [ENEMY_A, ENEMY_B]


    map = BuildPatrol.build_map(origin_map_data)  # map
    heros = BuildPatrol.build_heros(hero)  # heros
    monster = BuildPatrol.build_monster(enemies)

    f = Game(heros, monster, map)

    f2 = Action()
    s = f2.hero_action(hero, enemies, maps)
    print(s)
