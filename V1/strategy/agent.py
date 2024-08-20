# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/26 14:20
from strategy.action import Action
from strategy.handler.attack import Attack


class Agent(object):

    def swap_specific_keys(self, d, key1, key2):
        if key1 not in d or key2 not in d:
            raise KeyError("Both keys must exist in the dictionary.")

        d[key1], d[key2] = d[key2], d[key1]
        return d

    def add_maps_block(self, state):
        maps = state["maps"]
        for m in [state["hero"] + state["monster"]]:
            m.move_position(m.position, state["maps"])

    def choice_hero_act(self, hero, state):
        hero = hero.dict()
        enemies = [_.dict() for _ in state["monster"]]
        maps = state["map"].view_from_y_dict()
        maps = Attack().convert_maps(maps)
        teammates = [_.dict() for _ in state["hero"] if _.HeroID != hero["HeroID"]]
        res = Action().get_action_steps(hero, teammates, enemies, maps)
        return res

    def choice_monster_act(self, hero, state):
        state = self.swap_specific_keys(state, "hero", "monster")
        hero = hero.dict()
        enemies = [_.dict() for _ in state["monster"]]
        maps = state["map"].view_from_y_dict()
        maps = Attack().convert_maps(maps)
        teammates = [_.dict() for _ in state["hero"] if _.HeroID != hero["HeroID"]]
        res = Action().get_action_steps(hero, teammates, enemies, maps)
        return res
