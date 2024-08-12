# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/5 11:14
from copy import deepcopy
from itertools import product
from collections import deque

from strategy.handler.attack import Attack
from strategy.handler.distance_func import DistanceFunc
from strategy.handler.func import BasicFunc
from strategy.handler.self_func import SelfFunc
from strategy.handler.skill_attack_range import SkillRange


class Move(object):
    def is_escape(self, hero, enemies, maps):
        # 是否需要逃跑
        hp = hero["Hp"]
        hp_base = hero["HpBase"]
        hero_position = tuple(hero["position"])
        enemies = [e for e in enemies if e["Hp"] > 0]

        atk_count = 0
        if SelfFunc().is_health_sub_half(hp, hp_base):
            for enemy in enemies:
                enemy_atk_range = SkillRange().get_attack_range(enemy, maps)
                if hero_position in enemy_atk_range:
                    atk_count += 1
                if atk_count > 1:
                    return True
        return False

    def find_closest_attack_position(self, hero, enemy_position, maps):
        enemy_position = tuple(enemy_position)
        hero_position = tuple(hero["position"])
        jump_height = int(hero["JumpHeight"][0])
        queue = deque([(hero_position, 0)])  # (current_position, current_distance)
        visited = set(hero_position)

        while queue:
            current_position, current_distance = queue.popleft()

            for dx, dy in product([-1, 1, 0, 0], [0, 0, -1, 1]):
                new_position = (current_position[0] + dx, current_position[1] + dy)
                if new_position in maps:
                    if BasicFunc().is_reach(hero, maps[new_position], jump_height):
                        point = tuple(maps[new_position]["position"])

                        _hero = deepcopy(hero)
                        _hero["position"] = point

                        stk_range = SkillRange().get_attack_range(_hero, maps)
                        if enemy_position in stk_range:
                            return point

                        if point not in visited:
                            visited.add(point)
                            queue.append((point, current_distance + 1))

        return None

    def choose_move_steps(self, hero, enemies, maps):
        position = tuple(hero["position"])
        round_action = int(hero["RoundAction"])
        doge_base = int(hero["DogBase"])
        jump_height = int(hero["JumpHeight"][0])
        enemies = [e for e in enemies if e["Hp"] > 0]
        if DistanceFunc().is_within_range(doge_base, position, enemies):
            closest_enemy_position = DistanceFunc().find_closest_enemy(position, enemies)

        else:
            print(f"警戒范围{doge_base}没有敌人, 检查BOSS位置")
            closest_enemy_position = [e for e in enemies if e.get("Quality") == 2]
            if closest_enemy_position:
                closest_enemy_position = closest_enemy_position[0]
            else:
                print(f"警戒范围{doge_base}外没有BOSS")

                return []
        atk_position = self.find_closest_attack_position(hero, closest_enemy_position["position"], maps)

        if atk_position:
            print(f"{hero['HeroID']}:{position}跳跃高度:{jump_height},警戒范围:{doge_base},本回合可移动{round_action},向敌人{closest_enemy_position['position']}移动, 移动目标: {atk_position}, 本次移动{move_steps}")

            move_steps = DistanceFunc().find_shortest_path(position, atk_position, jump_height, maps)[: round_action+1]
        else:
            return []

        # move_steps = DistanceFunc().manhattan_path(position, closest_enemy_position, round_action, maps, jump_height)
        return move_steps

    def escape(self, hero, enemies, maps):
        # 逃跑：当次可移动范围内，距离所有人敌人的距离平均值最远的位置
        position = tuple(hero["position"])
        round_action = hero["RoundAction"]

        jump_height = int(hero["JumpHeight"][0])

        enemies_position = [tuple(e["position"]) for e in enemies]
        move_steps = DistanceFunc().get_furthest_position(position, enemies_position, round_action, maps, jump_height)
        print(f'{hero["HeroID"]}向{move_steps}逃跑')
        return move_steps

