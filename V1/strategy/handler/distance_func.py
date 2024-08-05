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
    def find_closest_enemy(hero_position, enemy_positions):
        # 获取距离最近的敌人
        closest_enemy = None
        min_distance = float('inf')

        for enemy in enemy_positions:
            distance = BasicFunc().manhattan_distance(hero_position, enemy)
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy

        return closest_enemy

    @staticmethod
    def is_within_attack_range(range, hero_position, enemies):
        # 当前攻击(普攻 OR 技能 OR 警戒)范围内的敌人列表
        count = []
        for enemy in enemies:
            if enemy["Hp"] > 0:
                enemy_position = enemy["position"]
                if BasicFunc().manhattan_distance(hero_position, enemy_position) <= range:
                    count.append(enemy)
        return count

    @staticmethod
    def manhattan_path(start, end, steps):
        x1, y1, z1 = start
        x2, y2, z2 = end

        path = []
        x, y, z = x1, y1, z1

        while (x != x2 or y != y2) and steps > 0:
            if x < x2:
                x += 1
            elif x > x2:
                x -= 1
            elif y < y2:
                y += 1
            elif y > y2:
                y -= 1

            path.append((x, y, z))
            steps -= 1

        return path

if __name__ == '__main__':
    hero_position = (1, 1, 1)
    enemy_positions = (5, 7, 5)
    f = DistanceFunc()
    print(f.manhattan_path(hero_position, enemy_positions, 6))