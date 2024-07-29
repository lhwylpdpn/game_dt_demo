# HERO = {
#     "HeroID": 1,
#     "Name": "Jinx",
#     "Hp": 80,
#     "HpBase": 100,
#     "skills": [{"SkillId": "治疗术", "range": 2, "max_uses": 3, "skill_type": "Recovery", "remainingUses": 0}, {"SkillId": "火球术", "range": 10, "max_uses": 3, "skill_type": "Attack", "remainingUses": 2}],
#     "AtkDistance": [0, 1],
#     "position": [1, 1, 1],
#     "max_step": 2,
#     "dogBase": 4
# }


HERO = {'skills': [{'effects': [{'id': 1, 'key': '', 'param': ['110'], 'tag': ''}], 'sn': 192, 'SkillId': 39, 'SkillLev': 1, 'skill_type': 'Attack' ,'SkillIcon': 'texture/icon\\skill\\fangyu3', 'SkillSpine': '', 'effecDescribe': '梅耶剑术造成的伤害增加<color=#faa755>10%</color>。', 'range': 2}], 'sn': 3, 'HeroID': 11003, 'Name': '法系女主', 'protagonist': 1, 'Hp': 24, 'HpBase': 24, 'position': [3, 5, 8], 'JumpHeight': [8, 8], 'max_step': 2, 'normal_attach_range': 2}


ENEMY_A= {'skills': [{'effects': [{'id': 1, 'key': '', 'param': ['0'], 'tag': ''}], 'sn': 170, 'SkillId': 30, 'SkillLev': 1, 'SkillSpine': '', 'range': 2}], 'sn': 1, 'MonsterId': 1173, 'Name': '骷髅怪', 'protagonist': 0, 'Hp': 1000, 'Atk': 10, 'position': [5, 5, 7], 'JumpHeight': [6, 6], 'max_step': 2, 'normal_attack_range': 2}

# ENEMY_A = {
#     "MonsterId": 10,
#     "Name": "A",
#     "hp": 100,
#     "normal_attack_range": 10,
#     "position": (3, 3, 1)
# }
#
ENEMY_B = {
    "MonsterId": 11,
    "Name": "B",
    "Hp": 100,
    "normal_attack_range": 10,
    "position": (6, 6, 2),

}

MAPS = [(1, 1, 1), (1, 2, 1), (1, 3, 1), (2, 1, 1), (2, 2, 1), (2, 3, 1), (3, 1, 1), (3, 2, 1), (3, 3, 1)]
