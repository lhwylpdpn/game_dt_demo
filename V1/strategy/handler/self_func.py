# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:44
import math
from collections import deque

from V1.strategy.handler.distance_func import DistanceFunc
from V1.strategy.handler.func import BasicFunc


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
    def find_farthest_position(hero_position, enemies, map_blocks, max_steps):
        # 英雄距离所有人敌人的距离平均值最远的移动顺序
        max_distance_sum = -math.inf
        move_sequence = []  # 记录移动顺序

        # BFS队列，记录位置、当前步数和移动路径
        queue = deque([(hero_position, 0, [hero_position])])
        visited = set()
        visited.add(tuple(hero_position))

        while queue:
            current_position, current_steps, path = queue.popleft()
            if current_steps == max_steps:
                continue

            # 可移动的邻近位置
            possible_moves = SelfFunc().possible_moves(current_position)

            for move in possible_moves:
                if move in map_blocks and move not in visited:
                    visited.add(move)
                    new_path = path + [move]
                    distance_sum = sum(BasicFunc().manhattan_distance(move, enemy["position"]) for enemy in enemies)
                    if distance_sum > max_distance_sum:
                        max_distance_sum = distance_sum
                        move_sequence = new_path
                    queue.append((move, current_steps + 1, new_path))

        return move_sequence

    @staticmethod
    def can_skill_attack_multiple_enemies(hero_position, skills, enemies, map_blocks, max_steps):
        # 英雄技能能攻击到>1的敌人 OR 英雄移动X后, 技能能攻击到>1的敌人
        path = []
        skill_counts = []
        attack_enemies = []
        for skill in skills:
            skill_range = 3
            attack_enemies = DistanceFunc().is_within_attack_range(skill_range, hero_position, enemies)
            skill_counts.append(len(attack_enemies))

        # BFS队列，记录位置、当前步数、移动路径和使用的技能
        queue = deque([(hero_position, 0, [], None)])
        visited = set()
        visited.add(tuple(hero_position))

        while queue:
            current_position, current_steps, path, used_skill = queue.popleft()
            if current_steps == max_steps:
                continue

            # 判断当前位置是否满足技能攻击范围内有多个敌方单位的条件
            for idx, count in enumerate(skill_counts):
                if count >= 2:
                    attack_enemies = DistanceFunc().is_within_attack_range(skills[idx]["range"], hero_position, enemies)
                    return True, [], skills[idx]["SkillId"], attack_enemies

            possible_moves = SelfFunc().possible_moves(current_position)

            for move in possible_moves:
                if move in map_blocks and move not in visited:
                    visited.add(move)
                    new_path = path + [move]  # 记录新的移动路径

                    # 检查移动后是否能够攻击到两个敌人
                    can_attack_two_enemies = False
                    for idx, skill in enumerate(skills):
                        skill_range = skill["range"]
                        attack_enemies = DistanceFunc().is_within_attack_range(skill_range, move, enemies)
                        # if len(DistanceFunc().is_within_attack_range(skill_range, move, enemies)) >= 2:
                        if len(attack_enemies):
                            can_attack_two_enemies = True
                            used_skill = skill["SkillId"]
                            break

                    if can_attack_two_enemies:
                        return True, new_path, used_skill, attack_enemies

                    queue.append((move, current_steps + 1, new_path, used_skill)),

        return False, path, None, None

    @staticmethod
    def can_normal_attack_multiple_enemies(hero_position, attack_range, enemies, map_blocks, max_steps):
        # 英雄技能能攻击到>1的敌人 OR 英雄移动X后, 技能能攻击到>1的敌人
        path = []
        enemy_count = 1
        attack_enemies = DistanceFunc().is_within_attack_range(attack_range, hero_position, enemies)
        skill_counts = [len(attack_enemies)]

        queue = deque([(hero_position, 0, [], None)])
        visited = set()
        visited.add(tuple(hero_position))

        while queue:
            current_position, current_steps, path, used_skill = queue.popleft()
            if current_steps == max_steps:
                continue

            # 判断当前位置是否满足技能攻击范围内有多个敌方单位的条件
            for idx, count in enumerate(skill_counts):
                if count >= enemy_count:
                    return True, [], "普通攻击", attack_enemies

            possible_moves = SelfFunc().possible_moves(current_position)

            for move in possible_moves:
                if move in map_blocks and move not in visited:
                    visited.add(move)
                    new_path = path + [move]  # 记录新的移动路径
                    attack_enemies = DistanceFunc().is_within_attack_range(attack_range, hero_position, enemies)

                    # if len(DistanceFunc().is_within_attack_range(attack_range, move, enemies)) >= enemy_count:
                    if len(attack_enemies) >= enemy_count:
                        return True, new_path, "普通攻击", attack_enemies

                    queue.append((move, current_steps + 1, new_path, used_skill))

        return False, path, None, None

    @staticmethod
    def execute_heal():
        # 执行加血动作
        pass

    @staticmethod
    def escape(hero_position, enemies, map_blocks, max_steps):
        # 逃跑：当次可移动范围内，距离所有人敌人的距离平均值最远的位置
        return SelfFunc().find_farthest_position(hero_position, enemies, map_blocks, max_steps)

    @staticmethod
    def determine_direction(pos1, pos2):
        # 判断移动方向
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2

        if x2 == x1 + 1 and y2 == y1 and z2 == z1:
            return "RIGHT"
        elif x2 == x1 - 1 and y2 == y1 and z2 == z1:
            return "LEFT"
        elif y2 == y1 + 1 and x2 == x1 and z2 == z1:
            return "BOTTOM"
        elif y2 == y1 - 1 and x2 == x1 and z2 == z1:
            return "TOP"
        else:
            raise Exception("invalid move")

    @staticmethod
    def generate_pairs(lst):
        # 返回相邻数组
        return [(lst[i], lst[i + 1]) for i in range(len(lst) - 1)]

