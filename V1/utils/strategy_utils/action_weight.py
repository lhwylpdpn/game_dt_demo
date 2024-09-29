# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/30 17:13
from log.log import log_manager
from strategy.strategy_context import strategy_params
from utils.strategy_utils.basic_data import Data
from utils.strategy_utils.basic_utils import manhattan_distance

WEIGHT = "weight"


class ActionWeight(object):
    def __init__(self, role=None, teammates=None, enemies=None, maps=None):
        self.role = role
        self.enemies = enemies
        self.teammates = teammates
        self.maps = maps
        self.strategy_params = strategy_params().get_strategy_params(self.role["BaseClassID"])[0]

        self.allEnemiesWarningRange = set()  # 所有敌人的警戒范围的点位合集

        self.enemiesDistance = []  # 敌人距离列表
        self.enemiesHpPerc = []  # 敌人剩余血量列表
        self.enemiesAtk = []  # 敌人攻击力列表
        self.enemiesDef = []  # 敌人防御列表

        self.atkTargetsCount = []  # 可攻击到的敌人数量的列表
        self.atkedTargetsCount = []  # 可被攻击到的敌人数量的列表
        self.heightGapNum = []  # 高度差值列表
        self.shortestPathNum = []  # 可移动的数量的列表
        self.enemiesWainingPoint = []  # 在敌人警戒范围内的点的列表
        self.maxAtkEnemy = int
        self.maxDefEnemy = int

    def is_default_skill(self, skill):
        if skill["DefaultSkills"] == 1:
            return
        return False

    def enemy_type(self):
        self.maxAtkEnemy = max(self.enemies, key=lambda x: x['Atk'])["HeroID"]
        self.maxDefEnemy = max(self.enemies, key=lambda x: x['Def'])["HeroID"]

    def enemies_warning_range(self):
        """ 所有敌人的警戒范围合集(去重 """
        for _ in self.enemies:
            self.allEnemiesWarningRange.update(_["warning_range"])
        self.allEnemiesWarningRange = set(self.allEnemiesWarningRange)

    def enemies_distance(self):
        """ 本次 所有敌人的距离列表 """
        self.enemiesDistance = [
            manhattan_distance(
                Data.value("position", self.role),
                Data.value("position", e),
            ) for e in self.enemies
        ]

    def enemies_hp_perc(self):
        """ 本次 所有敌人的血量比例 """
        self.enemiesHpPerc = [e["Hp"] / e["HpBase"] for e in self.enemies]

    def enemies_atk(self):
        """ 本次 所有敌人的攻击力 """
        self.enemiesAtk = [e["Atk"] for e in self.enemies]

    def enemies_def(self):
        """ 本次 所有敌人的防御力 """
        self.enemiesDef = [e["Def"] for e in self.enemies]

    def atk_targets_count(self, data):
        """ 每次选择 导致的可攻击到的敌人的数量的列表 """
        self.atkTargetsCount = [len(_["target"]) for _ in data]

    def atked_targets_count(self, data):
        """ 每次选择 导致的可被多少个敌人攻击到的数量的列表 """
        for _ in data:
            _count = 0
            for e in self.enemies:
                if _["hero_pos"] in e["warning_range"]:
                    _count += 1
            self.atkedTargetsCount.append(_count)

    def shortest_path_num(self, data):
        self.shortestPathNum = list(set([len(_["route"]) for _ in data]))

    def enemies_waining_point(self, data):
        """ 每次选择移动点位 中在敌人警戒范围的的点位数量的列表 """
        for _ in data:
            p = _["route"]
            c = self.allEnemiesWarningRange.intersection(set(p))
            self.enemiesWainingPoint.append(len(c))

    def height_gap_num(self):
        self.heightGapNum = [self.role["position"][2] - _["position"][2] for _ in self.enemies]

    def normalize_value(self, value, values):
        # 线性⬆
        min_value = min(values)
        max_value = max(values)
        if value - min_value == 0:
            return 0
        return round((value - min_value) / (max_value - min_value), 4)

    def inverse_normalize_value(self, value, values):
        # 线性⬇
        min_value = min(values)
        max_value = max(values)
        if value - min_value == 0 or max_value - min_value == 0:
            return 1
        score = round(1 - (value - min_value) / (max_value - min_value), 4)
        return score

    def atk_target(self, enemy):
        # 选择攻击对象的策略
        score = 0
        atk_target = self.strategy_params["atk_target"]
        if "nearest" in atk_target:
            _score = self.normalize_value(
                manhattan_distance(
                    Data.value("position", self.role),
                    Data.value("position", enemy)
                ),
                self.enemiesDistance
            )
            score += _score * atk_target["nearest"][WEIGHT]

        if "min_hp" in atk_target:
            _score = self.inverse_normalize_value(
                enemy["Hp"] / enemy["HpBase"],
                self.enemiesHpPerc
            )
            score += _score * atk_target["min_hp"][WEIGHT]

        if "max_atk" in atk_target:
            _score = self.normalize_value(
                enemy["Atk"],
                self.enemiesAtk
            )
            score += _score * atk_target["max_atk"][WEIGHT]

        if "max_def" in atk_target:
            _score = self.inverse_normalize_value(
                enemy["Def"],
                self.enemiesDef
            )
            score += _score * atk_target["max_def"][WEIGHT]

        if "career_support" in atk_target:
            if Data.value("ClassType3", enemy) == 3:
                score += atk_target["career_support"]["score"][1] * atk_target["career_support"][WEIGHT]

        if "career_attack" in atk_target:
            if Data.value("ClassType3", enemy) == 2:
                score += atk_target["career_attack"]["score"][1] * atk_target["career_attack"][WEIGHT]

        if "career_defense" in atk_target:
            if Data.value("ClassType3", enemy) == 1:
                score += atk_target["career_defense"]["score"][1] * atk_target["career_defense"][WEIGHT]

        if "non_elite" in atk_target:
            if Data.value("Quality", enemy) != 2:
                score += atk_target["non_elite"]["score"][1] * atk_target["non_elite"][WEIGHT]

        if "elite" in atk_target:
            if Data.value("Quality", enemy) == 2:
                score += atk_target["elite"]["score"][1] * atk_target["elite"][WEIGHT]

        # exclusive类型 TODO #####  尽量不攻击敌人, 避免在非战斗状态下攻击敌人

        return score

    def atk_type(self, skill, enemies):
        # 选择攻击方式
        score = 0
        atk_type = self.strategy_params["atk_type"]
        if "skill" in atk_type:
            _score = 0 if self.is_default_skill(skill) else 1
            score += _score * atk_type["skill"][WEIGHT]

        if "normal" in atk_type:
            _score = 1 if self.is_default_skill(skill) else 0
            score += _score * atk_type["normal"][WEIGHT]
        if "HIT_LINE" not in skill["effects"] and "HIT_RANGE" not in skill["effects"]:
            if len(enemies) == 1:
                if "single_max_atk" in atk_type:
                    if enemies[0]["HeroID"] == self.maxAtkEnemy:
                        score += atk_type["single_max_atk"][WEIGHT] * atk_type["single_max_atk"]["score"][1]
                if "single_max_def" in atk_type:
                    if enemies[0]["HeroID"] == self.maxDefEnemy:
                        score += atk_type["single_max_def"][WEIGHT] * atk_type["single_max_def"]["score"][1]
                if "single_career_support" in atk_type:
                    if Data.value("ClassType3", enemies[0]) == 3:
                        score += atk_type["single_career_support"][WEIGHT] * atk_type["single_career_support"]["score"][1]
                if "single_career_attack" in atk_type:
                    if Data.value("ClassType3", enemies[0]) == 2:
                        score += atk_type["single_career_attack"][WEIGHT] * atk_type["single_career_attack"]["score"][1]
                if "single_career_defense" in atk_type:
                    if Data.value("ClassType3", enemies[0]) == 1:
                        score += atk_type["single_career_defense"][WEIGHT] * atk_type["single_career_defense"]["score"][1]

        return score

    def move_position(self, atk_step):
        score = 0
        atk_targets = atk_step["target"]  # 攻击到的敌人list
        height_gap = self.role["position"][2] - atk_step["hero_pos"][2]
        move_position = self.strategy_params["move_position"]
        if "atk_multi" in move_position:
            _score = self.normalize_value(
                len(atk_targets),
                self.atkTargetsCount
            )
            score += _score * move_position["atk_multi"][WEIGHT]

        if "no_atk" in move_position:
            atked_count = 0
            for e in self.enemies:
                if self.role["position"] in e["warning_range"]:
                    atked_count += 1

            _score = self.inverse_normalize_value(
                atked_count,
                self.atkedTargetsCount
            )
            score += _score * move_position["no_atk"][WEIGHT]

        if "high" in move_position:
            _score = self.inverse_normalize_value(
                height_gap,
                self.heightGapNum
            )
            score += _score * move_position["high"][WEIGHT]
        # print(f"move_position: {round(score, 4)}")
        return score

    def move_path(self, move_step):
        score = 0
        move_path = self.strategy_params["move_path"]

        if "shortest" in move_path:
            _score = self.inverse_normalize_value(
                len(move_step),
                self.shortestPathNum
            )
            score += _score * move_path["shortest"][WEIGHT]

        if "no_warning" in move_path:
            _score = self.inverse_normalize_value(
                len(self.allEnemiesWarningRange.intersection(set(move_path))),
                self.enemiesWainingPoint
            )
            score += _score * move_path["no_warning"][WEIGHT]
        # print(f"move_path: {round(score, 4)}")
        return score

    def assist(self, step):
        score = 0
        assist = self.strategy_params["assist"]
        skill = step["skill"]
        if "single_heal" in assist:
            if "HIT_LINE" not in skill["effects"] and "HIT_RANGE" not in skill["effects"]:
                score += assist["single_heal"][WEIGHT] * assist["single_heal"]["score"][1]
        if "group_heal" in assist:
            if "HIT_LINE" in skill["effects"] or "HIT_RANGE" in skill["effects"]:
                score += assist["group_heal"][WEIGHT] * assist["group_heal"]["score"][1]

        # TODO 持续治疗

        if "assist_career_defense" in assist:
            for r in step["target"]:
                if Data.value("ClassType3", r) == 1:
                    score += assist["assist_career_defense"][WEIGHT] * assist["assist_career_defense"]["score"][1]

        if "assist_career_attack" in assist:
            for r in step["target"]:
                if Data.value("ClassType3", r) == 2:
                    score += assist["assist_career_attack"][WEIGHT] * assist["assist_career_attack"]["score"][1]

        if "self_heal" in assist:
            score += assist["self_heal"][WEIGHT] * assist["self_heal"]["score"][1]
        return score

    def select_attack_strategy(self, atk_data):
        weight = 0
        pick_data = None

        self.enemies_distance()
        self.enemies_hp_perc()
        self.enemies_atk()
        self.atk_targets_count(atk_data)
        self.atked_targets_count(atk_data)
        self.height_gap_num()
        self.enemies_warning_range()
        self.enemies_waining_point(atk_data)
        self.shortest_path_num(atk_data)
        self.enemy_type()

        if isinstance(self.strategy_params, dict):
            for each in atk_data:
                # print("-----WEIGHT-----")
                _weight = 0
                skill = each["skill"]
                move_path = each["route"]
                enemies = each["target"]

                if "atk_target" in self.strategy_params:
                    for e in enemies:
                        _weight += self.atk_target(e)

                if "atk_type" in self.strategy_params:
                    _weight += self.atk_type(skill, enemies)

                if "move_position" in self.strategy_params:
                    _weight += self.move_position(each)

                if "move_path" in self.strategy_params:
                    _weight += self.move_path(move_path)

                # print(f"_weight: {round(_weight, 2)}")
                if _weight >= weight:  # 筛选出权重最大的
                    pick_data = each

        # return pick_data
        return {"weight": weight, "data": pick_data}

    def select_assist_strategy(self, data):
        weight = 0
        pick_data = None
        if isinstance(self.strategy_params, dict):
            for each in data:
                _weight = 0
                if "assist" in self.strategy_params:
                    _weight += self.assist(each)

                if _weight >= weight:  # 筛选出权重最大的
                    pick_data = each

        return {"weight": weight, "data": pick_data}


if __name__ == '__main__':
    from utils.strategy_utils.range import Range

    s = strategy_params().get_strategy_params(2)[0]
