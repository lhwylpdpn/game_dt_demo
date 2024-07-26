# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/26 14:20
from V1.strategy.action import Action


class Agent(object):

    def choice_hero_act(self, hero, enemies, maps):
        return Action().hero_action(hero, enemies, maps)

    def choice_monster_act(self):
        return Action().monster_action()
