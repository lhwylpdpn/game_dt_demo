# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/5 11:14
from strategy.handler.distance_func import DistanceFunc
from strategy.handler.self_func import SelfFunc
from strategy.handler.skill_attack_range import SkillRange


class Move(object):
    def is_escape(self, hero, enemies, maps):
        # 是否需要逃跑
        hp = hero["Hp"]
        hp_base = hero["HpBase"]
        hero_position = tuple(hero["position"])
        atk_count = 0
        if SelfFunc().is_health_sub_half(hp, hp_base):
            for enemy in enemies:
                enemy_atk_range = SkillRange().get_attack_range(enemy, maps)
                if hero_position in enemy_atk_range:
                    atk_count += 1
                if atk_count > 1:
                    return True
        return False

    def choose_move_steps(self, hero, enemies, maps):
        position = tuple(hero["position"])
        round_action = hero["RoundAction"]
        doge_base = hero["DogBase"]
        jump_height = int(hero["JumpHeight"][0])

        enemy_positions = [tuple(e["position"]) for e in enemies]

        if DistanceFunc().is_within_range(doge_base, position, enemies):
            closest_enemy_position = DistanceFunc().find_closest_enemy(position, enemy_positions)
            print(f"{hero['HeroID']}向最近的敌人移动：{position} >>> {closest_enemy_position}")

        else:
            closest_enemy_position = [tuple(e["position"]) for e in enemies if e["Quality"] == 2][0]
            print(f"{hero['HeroID']}向BOSS移动:{position} >>> {closest_enemy_position}")

        move_steps = DistanceFunc().manhattan_path(position, closest_enemy_position, round_action, maps, jump_height)
        return move_steps

    def escape(self, hero, enemies, maps):
        # 逃跑：当次可移动范围内，距离所有人敌人的距离平均值最远的位置
        position = tuple(hero["position"])
        round_action = hero["RoundAction"]

        jump_height = int(hero["JumpHeight"][0])

        enemies_position = [tuple(e["position"]) for e in enemies]
        move_steps = DistanceFunc().get_furthest_position(position, enemies_position, round_action, maps, jump_height)
        print('逃跑')
        return move_steps

