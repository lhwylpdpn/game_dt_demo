# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/22 10:59
import copy

from strategy.action import Action


class Game(object):
    def __init__(self, hero: list, monster: list, maps, attachment, setting):
        self.hero = hero
        self.monster = monster
        self.map = maps
        self.attachment = attachment
        self.setting = setting
        self.hero_state = {
            "hero": self.hero,
            "monster": self.monster,
            "maps": self.map,
            "attachment": self.attachment,
            "setting": self.setting,
        }
        self.monster_state = {
            "hero": self.monster,
            "monster": self.hero,
            "maps": self.map,
            "attachment": self.attachment,
            "setting": self.setting,
        }

        self.hero_copy = copy.deepcopy(hero)
        self.monster_copy = copy.deepcopy(monster)
        self.map_copy = copy.deepcopy(maps)
        self.attachment_copy = copy.deepcopy(attachment)
        self.setting_copy = copy.deepcopy(setting)

    def reset(self):
        self.hero = copy.deepcopy(self.hero_copy)
        self.monster = copy.deepcopy(self.monster_copy)
        self.map = copy.deepcopy(self.map_copy)
        self.attachment_copy = copy.deepcopy(self.attachment)
        self.setting_copy = copy.deepcopy(self.setting)
        self.hero_state = {
            "hero": self.hero,
            "monster": self.monster,
            "maps": self.map,
            "attachment": self.attachment,
            "setting": self.setting
        }
        self.monster_state = {
            "hero": self.monster,
            "monster": self.hero,
            "maps": self.map,
            "attachment": self.attachment,
            "setting": self.setting
        }


    def _check_position(self):
        # 检查敌我双方位置是否在表面上
        maps = self.map.view_from_y_dict()
        for each in self.monster + self.hero:
            if tuple(each.position) not in maps:
                print(f"{each.position}不在地块表面！")
                return False
        return True

    def _check_hp(self):
        # 检查敌我双方 血量>0
        for each in self.monster + self.hero:
            if each.Hp < 0:
                print(f"存在血量为0的对象在场上")
                return False
        return True

    def _check_position_duplicate(self):
        # 检查敌我双方位置是否重复
        maps = self.map.view_from_y_dict()
        for each in self.monster + self.hero:
            if tuple(each.position) not in maps:
                print(f"{each.position} 人物位置重复")
                return False
        return True

    def hero_action(self, hero, step):
        if hero.is_death:
            return {"action_type": "HERO_DIED", "steps": "英雄死亡, 当前无行动"}
        res = Action().run_action(step, hero, self.hero_state)
        print(f"HERO >> 行动结束返回:{res}")
        return res

    def monster_action(self, hero, step):
        if hero.is_death:
            return {"action_type": "HERO_DIED", "steps": "英雄死亡, 当前无行动"}
        res = Action().run_action(step, hero, self.monster_state)
        print(f"MONSTER >> 行动结束返回:{res}")

        return res

    def check_game_over(self):
        monster = [m for m in self.monster if m.Quality == 2 and not m.is_death]
        if not monster:
            return True, 1

        hero = [h for h in self.hero if not h.is_death]

        if not hero:
            return True, 0

        return False, 2

    def get_current_alive_hero(self):
        roles = [h for h in self.hero if not h.is_death] + [m for m in self.monster if not m.is_death]
        return sorted(roles, key=lambda x: x.HeroID)

    def get_current_state(self):
        return {"hero": self.hero, "monster": self.monster, "map": self.map, "attachment": self.attachment, "setting": self.setting}

    def start(self):
        for each in self.hero:
            each.join_game(self.hero_state)
        for each in self.monster:
            each.join_game(self.monster_state)
        if not self._check_position():
            return False
        if not self._check_position_duplicate():
            return False
        if not self._check_hp():
            return False
        return True
