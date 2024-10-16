# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/26 14:20
from strategy.action import Action
from strategy.handler.attack import Attack
from strategy.level1_tree import make_decision as level1_make_decision
from strategy.level0_tree import make_decision as level0_make_decision
class Agent(object):

    def swap_specific_keys(self, d, key1, key2):
        d2 = {}
        if key1 not in d or key2 not in d:
            raise KeyError("Both keys must exist in the dictionary.")

        d2[key1], d2[key2] = d[key2], d[key1]
        d2["map"] = d["map"]
        return d2

    def add_maps_block(self, state):
        maps = state["maps"]
        for m in [state["hero"] + state["monster"]]:
            m.move_position(m.position, state["maps"])

    def choice_hero_act(self, hero, state,performance=None):
        print('------------------------------')
        hero = hero.dict()
        res =level0_make_decision(hero, state,performance=performance)
        if len(res)==0:
            res = level1_make_decision(hero, state,performance=performance)
        return res

    def choice_monster_act(self, hero, state,performance=None):
        state = self.swap_specific_keys(state, "hero", "monster")
        hero = hero.dict()
        res = level0_make_decision(hero, state,performance=performance)
        if len(res)==0:
            res = level1_make_decision(hero, state,performance=performance)
        return res