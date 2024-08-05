# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/1 15:51
from pprint import pprint

from V1.buildpatrol import BuildPatrol
from V1.strategy.handler.skill_attack_range import SkillRange
from V1.strategy.handler.weight import Weight
from V1.test_hero_data import origin_hero_data
from V1.test_map_data import origin_map_data
from V1.test_monster_data import origin_monster_data


class Attack(object):

    def convert_maps(self, maps):
        return {(x, y): {"z": z} for x, y, z in maps}

    def get_damage_skills(self, hero):
        """ 获取主动的可用技能 """
        s = []
        available_skills = hero["AvailableSkills"]
        for skill in hero["skills"]:
            if skill["SkillId"] in available_skills:
                if skill["ActiveSkills"] == 1:
                    if skill["DefaultSkills"] == 1:
                        s.append(skill)
                    else:
                        if int(skill["effects"]["USE_COUNT"]["param"][0]) > 1:
                            s.append(skill)
        return s

    def find_targets_within_atk_range(self, hero, enemies, maps):
        pick = {}
        skills = self.get_damage_skills(hero)
        max_step = hero["RoundAction"]
        position = tuple(hero["position"])
        jump_height = int(hero["JumpHeight"][0])
        move_positions = SkillRange.get_manhattan_path(*position, max_step, maps, jump_height)  # 英雄可移动到的点位
        print('----->', len(move_positions))

        for move, paths in move_positions.items():
            for skill in [skills[1]]:  # TODO test
                pick_list = SkillRange().get_all_possible_attacks(move, enemies, skill, maps, paths)
                for each in pick_list:
                    _weight = Weight().clac_skill_weight(each)
                    if not pick:
                        pick = {"weight": _weight, "data": each}
                        continue
                    if pick["weight"] < _weight:
                        pick = {"weight": _weight, "data": each}

        return pick["data"]

    def select_atk_target(self, pick_list):
        pass

if __name__ == '__main__':

    f = Attack()

