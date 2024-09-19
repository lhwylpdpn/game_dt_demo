# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/9/6 15:20

step_dict = {
    "action": {
        "enemy": {
            "normal": bool,
            "skill": {
                "any_attack": bool,
                "attack": [0, 1],  # 0单体，1群体
                "de_buff": [0, 1],  # 0单体，1群体
                "select": []  # 技能ID
            },
            "item": {
                "attack": [0, 1],
                "de_buff": [0, 1],
                "select": []
            }
        },
        "us": {
            "skill": {
                "any": bool,  # 可以对我方释放的技能
                "any_heal": [0, 1],  # 0单体，1群体
                "any_buff": [0, 1],  # 0单体，1群体
                "select": []  # 技能ID
            },
            "item": {
                "any": bool,
                "any_heal": [0, 1],
                "any_buff": [0, 1],
                "select": []  # 物品ID

            }
        }
    },
    "target": {
        "character": {
            "any": bool,
            "type": ["any", "前卫", "后卫"],
            "geo": ["any", "攻击型..."],
            "role": [],
            "select": []  # 指定类型
        },
        "role_type": []  # 精英，boss，普通

    },
    "filter": {
        "hp": {
            "max_hp": bool,
            "min_hp": bool,
            "max_perc_hp": bool,
            "min_perc_hp": bool,
            "hp_below": float,
            "hp_above": float
        },
        "status": {
            "any_buff": [],
            "any_de_buff": [],
            "no_status": bool
        },
        "distance": str,  # MIN / MAX
        "count": int,
        "value": {
            "p_attack": str,  # MIN / MAX
            "m_attack": str,  # MIN / MAX
            "p_defense": str,  # MIN / MAX
            "m_defense": str,  # MIN / MAX
            "speed": []  # TODO ？
        },
        "limit": {
            # TODO 行为限制
        }
    }
}


class SimpleStrategy(object):
    def __init__(self, role=None, teammates=None, enemies=None, maps=None):
        self.role = role
        self.enemies = enemies
        self.teammates = teammates
        self.maps = maps

    def atk_skills(self):
        s = []
        available_skills = self.role.get("AvailableSkills", [])
        for skill in self.role["skills"]:
            if skill["SkillId"] in available_skills:
                if skill["ActiveSkills"] == 1:
                    if "ATK_DISTANCE" in skill["effects"]:
                        if skill["DefaultSkills"] == 1:  # 普攻
                            s.append(skill)
                        else:
                            if int(skill["use_count"]) > 1:
                                s.append(skill)
        self.atk_skills = s

    def available_skills(self, nums):
        for s in self.atk_skills:
            if 1 in nums:  # 单体技能
                if "HIT_LINE" in s["effects"] and "HIT_RANGE" in s["effects"]:
                    self.atk_skills.remove(s)

            if 2 in nums:  # 群体技能
                if "HIT_LINE" not in s["effects"] and "HIT_RANGE" not in s["effects"]:
                    self.atk_skills.remove(s)

            if 3 in nums:  # 战士劈砍
                self.atk_skills = [_ for _ in self.atk_skills if _["SkillId"] == 78]

    def action_enemy(self, action_enemy, ):
        if "normal" in action_enemy:
            if action_enemy["normal"]:
                self.atk_skills = "普攻"  # ## ## TODO

    def filter_hp(self, hp_dict, roles):
        select = []
        if "max_hp" in hp_dict:
            select = max(roles, key=lambda x: x['Hp'])
        if "min_hp" in hp_dict:
            select = min(roles, key=lambda x: x['Hp'])
        if "max_perc_hp" in hp_dict:
            select = max(roles, key=lambda x: x['Hp'] / x['HpBase'])
        if "min_perc_hp" in hp_dict:
            select = min(roles, key=lambda x: x['Hp'] / x['HpBase'])
        if "hp_below" in hp_dict:
            select = [entry for entry in roles if (entry['hp'] / entry['hp_base']) > hp_dict["hp_below"]]
        if "hp_above" in hp_dict:
            select = [entry for entry in roles if (entry['hp'] / entry['hp_base']) < hp_dict["hp_below"]]
        return select



