# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/22 17:32
import random


class BasicFunc(object):
    @staticmethod
    def manhattan_distance(point1, point2):
        # 曼哈顿距离计算
        point1, point2 = tuple(point1), tuple(point2)
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    @staticmethod
    def is_reach(start, end, jump_height):
        # 是否可到达
        if abs(start[2] - end["position"][2]) < jump_height:
            if end["Block"] == 1:
                return True
        return False

    @staticmethod
    def find_closest_enemy(start, targets, z_diff):
        """ 查找距离start 高低差内 最近的点位 """
        filtered_enemies = [enemy for enemy in targets if abs(enemy[2] - start[2]) <= z_diff]
        if not filtered_enemies:
            return None
        closest_enemy = min(filtered_enemies, key=lambda enemy: BasicFunc().manhattan_distance(enemy, start))
        return closest_enemy

    @staticmethod
    def get_damage_skills(hero):
        #  获取主动的可用的攻击技能
        s = []
        available_skills = hero.get("AvailableSkills", [])
        for skill in hero["skills"]:
            if skill["SkillId"] in available_skills:
                if skill["ActiveSkills"] == 1:
                    if "ATK_DISTANCE" in skill["effects"]:
                        if skill["DefaultSkills"] == 1:
                            s.append(skill)
                        else:
                            if int(skill["effects"]["USE_COUNT"]["param"][0]) > 1:
                                s.append(skill)
        return s


if __name__ == '__main__':
    f = BasicFunc()
    print(f.find_closest_enemy((1,1,1), [(1, 2, 1), (1, 2, 1), (2, 2, 1)]))