# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:40

class SkillFunc(object):
    @staticmethod
    def can_heal_skill(skills):
        # 是否有回血技能 TODO 写死
        for s in skills:
            if s["skill_type"] == "Recovery" and s["remainingUses"] > 0:
                return True
        return False

    @staticmethod
    def has_attack_skill_available(skills):
        # 是否有可用攻击技能
        for s in skills:
            if s["skill_type"] == "Attack" and s["remainingUses"] > 0:
                return True
        return False

    @staticmethod
    def get_enemy_count_in_skill_range():
        # 获取技能范围内可攻击敌人的数量
        pass

    @staticmethod
    def cast_skill():
        # 施放技能
        pass
