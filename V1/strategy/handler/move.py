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
        """
        获取对于攻击者来说能攻击到敌人最近的位置，并得到前往这个位置的在round_action行动内的前进列表
        """
        enemy_position = tuple(enemy_position)
        hero_position = tuple(hero["position"])
        jump_height = int(hero["JumpHeight"][0])
        round_action = int(hero["RoundAction"])
        attack_pos_dict = {}

        for xz in maps:
            point = tuple(maps[xz]["position"])
            _hero = deepcopy(hero)
            _hero["position"] = point

            stk_range = SkillRange().get_attack_range(_hero, maps)
            if enemy_position in stk_range:
                move_steps = DistanceFunc().find_shortest_path(hero_position, point, jump_height, maps)[: round_action + 1]
                if move_steps:
                    attack_pos_dict[point] = move_steps

        if attack_pos_dict:
            closest_pos = min(attack_pos_dict.keys(), key=lambda k: BasicFunc().manhattan_distance(k, hero_position))
            steps = attack_pos_dict[closest_pos]
            return closest_pos, steps
        else:
            print(f"攻击者位置{hero_position} 对于{enemy_position}无前进步骤")
            return None, None

    def choose_move_steps(self, hero, enemies, maps):
        position = tuple(hero["position"])
        round_action = int(hero["RoundAction"])
        doge_base = int(hero["DogBase"])
        jump_height = int(hero["JumpHeight"][0])
        enemies = [e for e in enemies if e["Hp"] > 0]
        if DistanceFunc().is_within_range(doge_base, position, enemies):
            closest_enemy_position = DistanceFunc().find_closest_enemy(position, enemies)
            print(f"警戒范围{doge_base}内存在敌人{closest_enemy_position['position']}")

        else:
            print(f"警戒范围{doge_base}内没有敌人, 检查BOSS位置")
            closest_enemy_position = [e for e in enemies if e.get("Quality") == 2]
            if closest_enemy_position:
                closest_enemy_position = closest_enemy_position[0]
                print(f"BOSS位置为{closest_enemy_position['position']}")

            else:
                print(f"警戒范围{doge_base}外也没有BOSS")

                return []
        atk_position, move_steps = self.find_closest_attack_position(hero, closest_enemy_position["position"], maps)

        if atk_position:
            print(f"{hero['HeroID']}:{position}跳跃高度:{jump_height},警戒范围:{doge_base},本回合可移动{round_action},向敌人{closest_enemy_position['position']}移动, 移动目标: {atk_position},攻击位置:{atk_position}, 本次移动{move_steps}")
            return move_steps
        else: return []

    def escape(self, hero, enemies, maps):
        # 逃跑：当次可移动范围内，距离所有人敌人的距离平均值最远的位置
        position = tuple(hero["position"])
        round_action = hero["RoundAction"]

        jump_height = int(hero["JumpHeight"][0])

        enemies_position = [tuple(e["position"]) for e in enemies]
        move_steps = DistanceFunc().get_furthest_position(position, enemies_position, round_action, maps, jump_height)
        print(f'{hero["HeroID"]}向{move_steps}逃跑')
        return move_steps

if __name__ == '__main__':

    f = Move()

    # print(SkillRange().get_attack_range(hero, maps))