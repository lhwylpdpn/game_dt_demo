# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:44

class SelfFunc(object):
    @staticmethod
    def possible_moves(current_position):
        # 可移动的邻近位置
        return [
            (current_position[0] + 1, current_position[1], current_position[2]),
            (current_position[0] - 1, current_position[1], current_position[2]),
            (current_position[0], current_position[1] + 1, current_position[2]),
            (current_position[0], current_position[1] - 1, current_position[2])
        ]

    @staticmethod
    def is_health_sub_half(hero_hp, hero_base_hp):
        # 血量是否低于50%
        if float(hero_base_hp / 2) < hero_hp:
            return False
        return True

    @staticmethod
    def execute_heal():
        # 执行加血动作
        pass

    @staticmethod
    def determine_direction(pos1, pos2):
        # 判断移动方向
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2

        if x2 == x1 + 1 and y2 == y1:
            return "RIGHT"
        elif x2 == x1 - 1 and y2 == y1:
            return "LEFT"
        elif y2 == y1 + 1 and x2 == x1:
            return "BOTTOM"
        elif y2 == y1 - 1 and x2 == x1:
            return "TOP"
        else:
            raise Exception("invalid move")

    @staticmethod
    def generate_pairs(lst):
        # 返回相邻数组
        return [(lst[i], lst[i + 1]) for i in range(len(lst) - 1)]

