# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/22 10:59
from buildpatrol import BuildPatrol
from strategy.action import Action
from test_map_data import origin_map_data


class Game(object):
    def __init__(self, hero: list, monster: list, maps):
        self.hero = hero
        self.monster = monster
        self.maps = maps

    def _check_position(self):
        # 检查敌我双方位置是否在表面上
        maps = self.maps.view_from_z_dict()
        for each in self.monster + self.hero:
            if tuple(each.position) not in maps:
                return False
        return True

    def _check_hp(self):
        # 检查敌我双方 血量>0
        for each in self.monster + self.hero:
            if each.Hp < 0:
                return False
        return True

    def _check_position_duplicate(self):
        # 检查敌我双方位置是否在表面上
        maps = self.maps.view_from_z_dict()
        for each in self.monster + self.hero:
            if tuple(each.position) not in maps:
                return False
        return True


    def hero_action(self, hero, step):
        if hero.is_death:
            return {"action_type": "HERO_DIED", "steps": "英雄死亡, 当前无行动"}
        res = Action().run_action(step, hero, self.monster)
        print(f"HERO >> 行动结束返回:{res}")
        return res

    def monster_action(self, hero, step):
        if hero.is_death:
            return {"action_type": "HERO_DIED", "steps": "英雄死亡, 当前无行动"}
        res = Action().run_action(step, hero, self.hero)
        print(f"MONSTER >> 行动结束返回:{res}")

        return res
        # pass

    def check_game_over(self):
        monster = [m for m in self.monster if not m.is_death]
        if not monster:
            return True

        hero = [h for h in self.hero if not h.is_death]

        if not hero:
            return True

        return False

    def get_current_alive_hero(self):
        return [h for h in self.hero if not h.is_death] + [m for m in self.monster if not m.is_death]

    def get_current_state(self):
        return {"hero": self.hero, "monster": self.monster, "map": self.maps}

    def start(self):
        if not self._check_position():
            return False
        if not self._check_position_duplicate():
            return False
        if not self._check_hp():
            return False
        return True


if __name__ == '__main__':
    from strategy.handler.constant import HERO, ENEMY_A, ENEMY_B, MAPS

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
