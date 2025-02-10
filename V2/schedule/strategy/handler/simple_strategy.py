# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/9/6 15:20
from schedule.utils.strategy_utils.basic_data import Data
from schedule.utils.strategy_utils.basic_utils import get_damage_skills, get_heal_skills, manhattan_distance
from schedule.utils.strategy_utils.range import Range

step_dict = {
    "action": {
        "enemy": {
            "normal": bool,
            "skill": {
                "any_attack": bool,
                "attack": int,  # 0单体，1群体
                "de_buff": int,  # 0单体，1群体
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
                "any_heal": int,  # 0单体，1群体
                "any_buff": int,  # 0单体，1群体
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
            "type": int, # ["any", "前卫", "后卫"] 1 2 3
            "geo": int, # ["any", "攻击型..."] 1 2 3
            "role": int,
            "select": []  # 指定类型?
        },
        "role_type": int   # 精英，boss，普通

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
            "any_buff": [], # BUFF_ADD_HP , BUFF_HP, 护盾暂无,BUFF_ATK,  ADD_ATK, ADD_DEF, BUFF_DEF，ADD_MAGICAL_DEF，BUFF_MAGICAL_DEF,BUFF_ROUND_ACTION
            "any_de_buff": [], # 暂时没有
            "no_status": bool
        },
        "distance": str,  # MIN / MAX
        "count": int,
        "value": {
            "p_attack": str,  # MIN / MAX
            "m_attack": str,  # MIN / MAX
            "p_defense": str,  # MIN / MAX
            "m_defense": str,  # MIN / MAX
            "speed": str,  # MIN / MAX
        },
        "limit": {
            # TODO 行为限制
        }
    }
}


class SimpleStrategy(object):
    # def __init__(self, role=None, teammates=None, enemies=None, maps=None):
    def __init__(self, role, state):
        self.r = Range(role, state)

        self.role = self.r.role
        self.enemies = self.r.enemies
        self.teammates = self.r.teammates
        self.maps = self.r.map
        self.damage_skills = get_damage_skills(role)
        self.heal_skills = get_heal_skills(role)

    def _buff_key(self, role):
        return [_["buff_key"] for _ in Data.value("buff", role)]

    def action_enemy(self, strategy):
        if not strategy.get("action", {}).get("enemy"):
            return

        enemy_dict = strategy["action"]["enemy"]
        if "normal" in enemy_dict:
            if enemy_dict["normal"]:
                self.damage_skills = [s for s in self.role["skills"] if s["DefaultSkills"] == 1]
        if "skill" in enemy_dict:
            for k, v in enemy_dict["skill"].items():
                if k == "any_attack":
                    pass
                if k == "attack":
                    if v == 0:
                        self.damage_skills = [s for s in self.damage_skills if "HIT_LINE" not in s["effects"] and "HIT_RANGE" not in s["effects"]]
                    if v == 0:
                        self.damage_skills = [s for s in self.damage_skills if "HIT_LINE"  in s["effects"] or "HIT_RANGE"  in s["effects"]]
                if k == "de_buff":  # TODO debuff
                    pass
                if k == "select":
                    self.damage_skills = [s for s in self.damage_skills if s["SkillId"] in v]
        if "item" in enemy_dict:  # TODO 使用物品
            pass

    def action_us(self, strategy):
        if not strategy.get("action", {}).get("us"):
            return

        us_dict = strategy["action"]["us"]

        if "skill" in us_dict:
            for k, v in us_dict["skill"].items():
                if k == "any_attack":
                    pass
                if k == "attack":
                    if v == 0:
                        self.heal_skills = [s for s in self.heal_skills if "HIT_LINE" not in s["effects"] and "HIT_RANGE" not in s["effects"]]
                    if v == 0:
                        self.heal_skills = [s for s in self.heal_skills if "HIT_LINE"  in s["effects"] or "HIT_RANGE"  in s["effects"]]
                if k == "de_buff":  # TODO debuff
                    pass
                if k == "select":
                    self.heal_skills = [s for s in self.heal_skills if s["SkillId"] in v]
        if "item" in us_dict:  # TODO 使用物品
            pass

    def target(self, roles, strategy):
        if not strategy.get("target", {}):
            return roles

        tar_dict = strategy["target"]
        if "character" in tar_dict:
            for k, v in tar_dict["character"].items():
                if k == "any":
                    return roles
                if k == "type":
                    if v == "any":
                        return roles
                    else:
                        roles = [e for e in roles if Data.value("ClassType2", e) == v]
                if k == "geo":
                    if v == "any":
                        return roles
                    else:
                        roles = [e for e in roles if Data.value("ClassType3", e) == v]
                if k == "role":
                    if v == "any":
                        return roles
                    else:
                        roles = [e for e in roles if Data.value("ClassType4", e) == v]

        if "role_type" in tar_dict:
            roles = [e for e in roles if Data.value("Quality", e) == tar_dict["role_type"]]

        return roles

    def filter(self, roles, strategy):
        select = []
        if not strategy.get("filter"):
            return roles
        filter_dict = strategy["filter"]
        if "hp" in filter_dict:
            hp_dict = filter_dict["hp"]
            if "max_hp" in hp_dict:
                select = max(roles, key=lambda x: x['Hp'])
            if "min_hp" in hp_dict:
                select = min(roles, key=lambda x: x['Hp'])
            if "max_perc_hp" in hp_dict:
                select = max(roles, key=lambda x: x['Hp'] / x['HpBase'])
            if "min_perc_hp" in hp_dict:
                select = min(roles, key=lambda x: x['Hp'] / x['HpBase'])
            if "hp_below" in hp_dict:
                select = [entry for entry in roles if (entry['Hp'] / entry['HpBase']) > hp_dict["hp_below"]]
            if "hp_above" in hp_dict:
                select = [entry for entry in roles if (entry['Hp'] / entry['HpBase']) < hp_dict["hp_above"]]

        if "status" in filter_dict:
            if "any_buff" in filter_dict["status"]:
                select = [r for r in roles if bool(set(self._buff_key(r)) & set(filter_dict["status"]["any_buff"]))]
            if "any_de_buff" in filter_dict["status"]:  # TODO de-buff
                pass
            if "no_status" in filter_dict["status"]:
                select = [r for r in roles if not r["buff"]]

        if "distance" in filter_dict:
            _d = 0
            for r in roles:
                if manhattan_distance(Data.value("position", self.role), Data.value("position", r)) > _d:
                    select = [r]

        if "count" in filter_dict:
            if len(roles) < filter_dict["count"]:
                return []

        if "value" in filter_dict:
            for k, v in filter_dict["value"].items():
                if k == "p_attack":
                    select = max(roles, key=lambda x: x['Atk']) if v == "MAX" else min(roles, key=lambda x: x['Atk'])
                if k == "m_attack":
                    select = max(roles, key=lambda x: x['MagicalAtk']) if v == "MAX" else min(roles, key=lambda x: x['MagicalAtk'])
                if k == "p_defense":
                    select = max(roles, key=lambda x: x['Def']) if v == "MAX" else min(roles, key=lambda x: x['Def'])
                if k == "m_defense":
                    select = max(roles, key=lambda x: x['MagicalDef']) if v == "MAX" else min(roles, key=lambda x: x['MagicalDef'])
                if k == "speed":
                    select = max(roles, key=lambda x: x['Velocity']) if v == "MAX" else min(roles, key=lambda x: x['Velocity'])

        if "limit" in filter_dict:  # TODO 行为限制
            pass

        return select

    def choice(self, strategy, target_type):
        if target_type == "enemy":
            self.action_enemy(strategy)
            roles = self.target(self.enemies, strategy)
            self.enemies = self.filter(roles, strategy)
            self.r.enemies = self.enemies
            pick = self.r.find_attack_target()
            print("enemy本次选择：", pick)
            return pick

        elif target_type == "team":
            self.action_us(strategy)
            roles = self.target(self.teammates + [self.role], strategy)
            self.teammates = self.filter(roles, strategy)
            self.teammates = [_ for _ in self.teammates if _["HeroID"] != self.role["HeroID"]]
            self.r.teammates = self.teammates
            pick = self.r.find_heal_target()
            print("team本次选择：", pick)
            return pick


        else:
            raise Exception(f"No Target.{target_type}")










