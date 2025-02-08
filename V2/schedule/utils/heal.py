# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/9/5 17:18

from utils.config import demo_skill


def heal(caster, target, skill):
    heal_amount = 0

    # 释放者属性
    caster_magical_atk = caster.MagicalAtk
    caster_atk = caster.Atk
    caster_hpbase = caster.HpBase

    # 受动者属性
    target_hpbase = target.HpBase

    if skill.SkillId == demo_skill['战士迎击姿态']:
        heal_amount = float(caster_hpbase * 0.3)  # 30%

    elif skill.SkillId == demo_skill['治疗大型治疗']:
        heal_amount = float(caster_magical_atk * 2.4)  # 240%

    elif skill.SkillId == demo_skill['治疗持续治疗']:
        heal_amount = float(target_hpbase * 0.083)  # 8.3%

    elif skill.SkillId == demo_skill['治疗强力治愈']:
        # heal_amount = float(caster_magical_atk * 1.5)  # 150%
        heal_amount = float(caster_atk * 1.5)  # 150%
    else:
        return [{'heal': heal_amount, "pre_heal": heal_amount, "msg": f"治疗函数未处理此技能:{skill.SkillId}"}]

    return [{'heal': heal_amount, "pre_heal": heal_amount}]
