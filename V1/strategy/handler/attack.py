# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/1 15:51
from strategy.game_utils import GameUtils
from strategy.handler.skill_attack_range import SkillRange
from strategy.handler.weight import Weight


class Attack(object):

    def convert_maps(self, maps):
        # return {(x, y): {"z": z} for x, y, z in maps}
        xy_dict = {}
        for k, v in maps.items():
            v["y"] = k[1]
            v["position"] = tuple(v["position"])
            xy_dict[(k[0], k[2])] = v
        return xy_dict

    def find_targets_within_atk_range(self, hero, enemies, maps):
        pick_list = []
        if GameUtils.is_enemies_in_warning_range(hero, enemies, maps):
            skills = GameUtils().get_damage_skills(hero)
            doge_base = int(hero["DogBase"])
            max_step = hero["RoundAction"]
            position = tuple(hero["position"])
            jump_height = int(hero["JumpHeight"][0])
            enemies = [e for e in enemies if e["Hp"] > 0]
            print(f"[ATK]警戒范围内存在敌人, 攻击者{hero['HeroID']}{position},警戒范围{doge_base}, 本回合可移动{max_step}, 跳跃高度:{jump_height},  本次可用技能:{len(skills)}")
            move_positions = SkillRange.get_manhattan_path(*position, max_step, maps, jump_height)  # 英雄可移动到的点位
            for move, paths in move_positions.items():
                for skill in skills:
                    pick_list += SkillRange().get_all_possible_attacks(move, enemies, skill, maps, paths)
        return pick_list

    def select_atk(self, pick_list):
        pick = {}

        for each in pick_list:
            _weight = Weight().clac_skill_weight(each)
            if not pick:
                pick = {"weight": _weight, "data": each}
                continue
            if pick["weight"] < _weight:
                pick = {"weight": _weight, "data": each}
        print(f"[ATK]攻击者在{pick['data']['hero_pos']}位置对{pick['data']['skill_pos']}位置施放技能[{pick['data']['skill']['SkillId']}], 需要移动{pick['data']['route']}")
        return pick["data"]


if __name__ == '__main__':
    f = Attack()
