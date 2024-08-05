# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/22 17:32
import random


class BasicFunc(object):
    @staticmethod
    def manhattan_distance(point1, point2):
        # 曼哈顿距离计算
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    @staticmethod
    def find_closest_enemy(start, targets, z_diff):
        """ 查找距离start 高低差内 最近的点位 """
        filtered_enemies = [enemy for enemy in targets if abs(enemy[2] - start[2]) <= z_diff]
        if not filtered_enemies:
            return None
        closest_enemy = min(filtered_enemies, key=lambda enemy: BasicFunc().manhattan_distance(enemy, start))
        return closest_enemy


if __name__ == '__main__':
    f = BasicFunc()
    print(f.find_closest_enemy((1,1,1), [(1, 2, 1), (1, 2, 1), (2, 2, 1)]))