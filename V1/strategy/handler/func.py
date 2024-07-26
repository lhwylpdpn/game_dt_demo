# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/22 17:32
import random


class BasicFunc(object):
    @staticmethod
    def manhattan_distance(point1, point2):
        # 曼哈顿距离计算
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
