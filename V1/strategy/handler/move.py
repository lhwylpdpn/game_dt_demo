# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/5 11:14
from copy import deepcopy

from log.log import LogManager
from strategy.game_utils import GameUtils
from strategy.handler.dict_utils import DictUtils
from strategy.handler.distance_func import DistanceFunc
from strategy.handler.skill_attack_range import SkillRange
from utils.strategy_utils.range import Range

log_manager = LogManager()


class Move(object):
    # @staticmethod
    # def is_health_sub_half(hero_hp, hero_base_hp):
    #     # 血量是否低于50%
    #     if float(hero_base_hp / 2) < hero_hp:
    #         return False
    #     return True
    #
    # def is_escape(self, hero, enemies, maps):
    #     # 是否需要逃跑
    #     hp = hero["Hp"]
    #     hp_base = hero["HpBase"]
    #     hero_position = tuple(hero["position"])
    #     enemies = [e for e in enemies if e["Hp"] > 0]
    #
    #     atk_count = 0
    #     if Move().is_health_sub_half(hp, hp_base):
    #         for enemy in enemies:
    #             enemy_atk_range = SkillRange().get_attack_range(enemy, maps)
    #             if hero_position in enemy_atk_range:
    #                 atk_count += 1
    #             if atk_count > 1:
    #                 return True
    #     return False
    #
    # def get_block_step(self, steps, block_status, maps):
    #     move_steps = []
    #     for k, s in enumerate(steps):
    #         xz = GameUtils.get_xz(s)
    #         if k > 0:
    #             if maps[xz]["Block"] not in block_status:
    #                 break
    #         move_steps.append(s)
    #     return move_steps
    #
    # def has_combat_ready_teammate(self, role, teammates, enemies, maps):
    #     # 获取在战斗状态的队友的位置
    #     distance = None
    #     teammate_position = None
    #     role_position = DictUtils.value("position", role)
    #
    #     for t in teammates:
    #         if GameUtils.is_in_combat(t, enemies, maps):
    #             _teammate_position = DictUtils.value("position", t)
    #             _distance = GameUtils.manhattan_distance(role_position, _teammate_position)
    #
    #             if distance and teammate_position:
    #                 if distance > _distance:
    #                     distance, teammate_position = _distance, _teammate_position
    #             else:
    #                 distance, teammate_position = _distance, _teammate_position
    #     return teammate_position
    #
    # def find_closest_attack_position(self, hero, enemy_position, maps):
    #     """
    #     获取对于攻击者来说能攻击到敌人最近的位置，并得到前往这个位置的在round_action行动内的前进列表
    #     """
    #     enemy_position = tuple(enemy_position)
    #     hero_position = DictUtils.value("position", hero)
    #     jump_height = DictUtils.value("JumpHeight", hero)
    #     round_action = DictUtils.value("RoundAction", hero)
    #     attack_pos_dict = {}
    #
    #     for xz in maps:
    #         point = tuple(maps[xz]["position"])
    #         _hero = deepcopy(hero)
    #         _hero["position"] = point
    #
    #         stk_range = SkillRange().get_attack_range(_hero, maps)
    #         if enemy_position in stk_range:
    #             move_steps = GameUtils.find_shortest_path(hero_position, point, jump_height, maps, [1, 2, 3])[: round_action + 1]
    #             if move_steps:
    #                 attack_pos_dict[point] = move_steps
    #
    #     if attack_pos_dict:
    #         closest_pos = min(attack_pos_dict.keys(), key=lambda k: GameUtils.manhattan_distance(k, hero_position))
    #         steps = attack_pos_dict[closest_pos]
    #         return closest_pos, steps
    #     else:
    #         return None, None
    #
    # def move_to_enemy(self, hero, teammates, enemies, maps):
    #     position = tuple(hero["position"])
    #     round_action = int(hero["RoundAction"])
    #     doge_base = int(hero["DogBase"])
    #     jump_height = int(hero["JumpHeight"][0])
    #     enemies = [e for e in enemies if e["Hp"] > 0]
    #     hero["skills"] = GameUtils.get_damage_skills(hero)
    #     if DistanceFunc().is_within_range(doge_base, position, enemies):
    #         closest_enemy_position = DistanceFunc().find_closest_enemy(position, enemies)
    #         print(f"[MOVE]警戒范围{doge_base}内存在敌人{closest_enemy_position['position']}")
    #         atk_position, move_steps = self.find_closest_attack_position(hero, closest_enemy_position["position"], maps)
    #         if atk_position:
    #             move_steps = self.get_block_step(move_steps, (1,), maps)
    #             if len(move_steps) > 1:
    #                 print(f"[MOVE]{hero['HeroID']}:{position}跳跃高度:{jump_height},警戒范围:{doge_base},本回合可移动{round_action},向敌人{closest_enemy_position['position']}移动, 移动目标: {atk_position},攻击位置:{atk_position}, 本次移动{move_steps}")
    #                 return True, move_steps
    #     return False, None
    #
    # def move_to_combat_teammate(self, hero, teammates, enemies, maps):
    #     position = tuple(hero["position"])
    #     round_action = int(hero["RoundAction"])
    #     doge_base = int(hero["DogBase"])
    #     jump_height = int(hero["JumpHeight"][0])
    #     enemies = [e for e in enemies if e["Hp"] > 0]
    #     hero["skills"] = GameUtils.get_damage_skills(hero)
    #     teammate_position = self.has_combat_ready_teammate(hero, teammates, enemies, maps)
    #     if teammate_position:
    #         print(f"[MOVE]存在战斗状态的队友: {teammate_position}")
    #         steps = GameUtils.find_shortest_path(position, teammate_position, jump_height, maps, [1, 2, 3])[: round_action + 1]
    #         move_steps = self.get_block_step(steps, (1,), maps)
    #         if len(move_steps) > 1:
    #             return True, move_steps
    #     return False, None
    #
    # def move_to_boss(self, hero, teammates, enemies, maps):
    #     position = tuple(hero["position"])
    #     round_action = int(hero["RoundAction"])
    #     doge_base = int(hero["DogBase"])
    #     jump_height = int(hero["JumpHeight"][0])
    #     enemies = [e for e in enemies if e["Hp"] > 0]
    #     hero["skills"] = GameUtils.get_damage_skills(hero)
    #     print(f"[MOVE]警戒范围{doge_base}内没有敌人, 检查BOSS位置")
    #     closest_enemy_position = [e for e in enemies if e.get("Quality") == 2]
    #     if closest_enemy_position:
    #         closest_enemy_position = closest_enemy_position[0]
    #         atk_position, move_steps = self.find_closest_attack_position(hero, closest_enemy_position["position"], maps)
    #         print(f"[MOVE]BOSS位置为{closest_enemy_position['position']}")
    #         if atk_position:
    #             print(f"[MOVE]{hero['HeroID']}:{position}跳跃高度:{jump_height},警戒范围:{doge_base},本回合可移动{round_action},向敌人{closest_enemy_position['position']}移动, 移动目标: {atk_position},攻击位置:{atk_position}, 本次移动{move_steps}")
    #             move_steps = self.get_block_step(move_steps, (1,), maps)
    #             if len(move_steps) > 1:
    #                 return True, move_steps
    #
    #     return False, None

    def is_escape(self, role, state):
        f = Range(role, state)
        if f.is_health_below_threshold(0.5):
            if f.nearby_enemy_count(1):
                return True
        return False

    def choose_move_steps(self, role, state):
        f = Range(role, state)
        print("[MOVE 选择：]")
        _bool, steps = f.move_to_enemy()
        if not _bool:
            _bool, steps = f.move_to_combat_teammate()
            if not _bool:
                _bool, steps = f.move_to_boss()

        if _bool:
            return steps
        else:
            # tmp = log_manager.add_log(log_data=str({"role": role, "state": state}) )
            # print(f"log tmp: {tmp}")
            return []

    # def choose_move_steps_old(self, hero, teammates, enemies, maps):
    #     position = tuple(hero["position"])
    #     round_action = int(hero["RoundAction"])
    #     doge_base = int(hero["DogBase"])
    #     jump_height = int(hero["JumpHeight"][0])
    #     enemies = [e for e in enemies if e["Hp"] > 0]
    #     hero["skills"] = GameUtils.get_damage_skills(hero)
    #
    #     if not hero["skills"]:
    #         print("当前英雄无可用技能！")
    #
    #     if DistanceFunc().is_within_range(doge_base, position, enemies):
    #         closest_enemy_position = DistanceFunc().find_closest_enemy(position, enemies)
    #         print(f"[MOVE]警戒范围{doge_base}内存在敌人{closest_enemy_position['position']}")
    #
    #     else:
    #         teammate_position = self.has_combat_ready_teammate(hero, teammates, enemies, maps)
    #         if teammate_position:
    #             steps = GameUtils.find_shortest_path(position, teammate_position, jump_height, maps, [1])[: round_action+1]
    #             move_steps = self.get_block_step(steps, (1,), maps)
    #             print(f"[MOVE]存在战斗状态的队友: {teammate_position}, 向队友移动:{move_steps}")
    #             return move_steps
    #
    #         else:
    #             print(f"[MOVE]警戒范围{doge_base}内没有敌人, 检查BOSS位置")
    #             closest_enemy_position = [e for e in enemies if e.get("Quality") == 2]
    #             if closest_enemy_position:
    #                 closest_enemy_position = closest_enemy_position[0]
    #                 print(f"[MOVE]BOSS位置为{closest_enemy_position['position']}")
    #
    #             else:
    #                 print(f"[MOVE]警戒范围{doge_base}外也没有BOSS")
    #                 return []
    #     atk_position, move_steps = self.find_closest_attack_position(hero, closest_enemy_position["position"], maps)
    #
    #     if atk_position:
    #         print(f"[MOVE]{hero['HeroID']}:{position}跳跃高度:{jump_height},警戒范围:{doge_base},本回合可移动{round_action},向敌人{closest_enemy_position['position']}移动, 移动目标: {atk_position},攻击位置:{atk_position}, 本次移动{move_steps}")
    #         return move_steps
    #     else:
    #         steps = GameUtils.find_shortest_path(position, closest_enemy_position["position"], jump_height, maps, [1, 2])[: round_action+1]
    #         move_steps = self.get_block_step(steps, (2,), maps)
    #
    #         if len(move_steps) > 1:
    #             return move_steps
    #         tmp = log_manager.add_log(log_data=str({"hero": hero, "map": maps, "enemies": enemies, "teammates": teammates}), )
    #         print(f"[MOVE]攻击者位置{position} 对于{closest_enemy_position['position']}无前进步骤, 可用技能为{len(hero['skills'])}, log_tmp: {tmp}")
    #         return []

    def escape(self, role, state):
        # 逃跑：当次可移动范围内，距离所有人敌人的距离平均值最远的位置
        f = Range(role, state)
        move_steps = f.get_furthest_position()
        print(f'{role["HeroID"]}向{move_steps}逃跑')
        return move_steps


if __name__ == '__main__':
    pass