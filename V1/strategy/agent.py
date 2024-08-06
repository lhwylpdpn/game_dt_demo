# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/26 14:20
from V1.strategy.action import Action
from V1.strategy.handler.attack import Attack


class Agent(object):

    def swap_specific_keys(self, d, key1, key2):
        if key1 not in d or key2 not in d:
            raise KeyError("Both keys must exist in the dictionary.")

        d[key1], d[key2] = d[key2], d[key1]
        return d

    def choice_hero_act(self, hero, state):
        hero = hero.dict()
        enemies = [_.dict() for _ in state["monster"]]
        used_points = [tuple(_.position) for _ in state["hero"]] + [tuple(_.position) for _ in state["monster"]]
        print('----->', used_points)
        maps = state["map"].view_from_z_dict()
        maps = Attack().convert_maps(maps, used_points)
        res = Action().get_action_steps(hero, enemies, maps)
        return res

    def choice_monster_act(self, hero, state):
        return []
        state = self.swap_specific_keys(state, "hero", "monster")
        hero = hero.dict_short()
        enemies = [_.dict_short() for _ in state["monster"]]
        maps = state["map"].list_land_postion()
        res = Action().get_action_steps(hero, enemies, maps)
        return res
