# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/22 10:59
from V1.strategy.action import Action


class Game(object):
    def __init__(self, hero: list, monster: list, maps):
        self.hero = hero
        self.monster = monster
        self.maps = maps

    def action(self, step):
        Action().run_action(step)

    def get_current_alive_hero(self):
        return [h for h in self.hero if not h.is_death()] + [m for m in self.monster if not m.is_death()]

    def get_current_state(self):
        return {"hero": self.hero, "monster": self.monster, "map": self.maps}

    def start(self, heroes, enemies, maps):
        pass
