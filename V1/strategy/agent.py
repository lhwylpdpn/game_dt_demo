# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/26 14:20
from V1.strategy.action import Action


class Agent(object):

    def choice_hero_act(self, hero, state):
        hero = hero.dict_short()
        enemies = [_.dict_short() for _ in state["monster"]]
        maps = state["map"].list_land_postion()
        return Action().hero_action(hero, enemies, maps)

    def choice_monster_act(self):
        return Action().monster_action()
