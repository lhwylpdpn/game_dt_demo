# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:41
from V1.strategy.handler.func import BasicFunc


class DistanceFunc(object):

    @staticmethod
    def is_within_enemy_range(hero_position, enemies):
        # 能攻击到英雄的敌人数量
        count = []
        for enemy in enemies:
            e_position = enemy["position"]
            e_atk_range = enemy["normal_attack_range"]

            if abs(e_position[0] - hero_position[0]) + abs(e_position[1] - hero_position[1]) <= e_atk_range:
                count.append(enemy)
        return count

    @staticmethod
    def is_within_attack_range(range, hero_position, enemies):
        # 当前攻击(普攻 OR 技能 OR 警戒)范围内的敌人列表
        count = []
        for enemy in enemies:
            enemy_position = enemy["position"]
            if BasicFunc().manhattan_distance(hero_position, enemy_position) <= range:
                count.append(enemy)
        return count