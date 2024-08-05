# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/5 11:14
from V1.strategy.handler.attack import Attack
from V1.strategy.handler.distance_func import DistanceFunc
from V1.strategy.handler.skill_attack_range import SkillRange
from V1.strategy.handler.weight import Weight


class Move(object):
    def choose_move_point(self, hero, enemies, maps):
        position = tuple(hero["position"])
        jump_height = int(hero["JumpHeight"][0])
        enemy_positions = [e["position"] for e in enemies]

        closest_enemy_position = DistanceFunc().find_closest_enemy(position, enemy_positions)

