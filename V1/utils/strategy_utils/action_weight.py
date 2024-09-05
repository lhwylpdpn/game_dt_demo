# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/30 17:13
from log.log import log_manager
from strategy.strategy_context import strategy_params
from utils.strategy_utils.basic_data import Data
from utils.strategy_utils.basic_utils import manhattan_distance
from utils.strategy_utils.range import Range

WEIGHT = "weight"


class ActionWeight(object):
    def __init__(self, role_id, role=None, teammates=None, enemies=None, maps=None):
        self.role = role
        self.enemies = enemies
        self.teammates = teammates
        self.maps = maps
        self.strategy_params = strategy_params().get_strategy_params(role_id)[0]

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

    def is_default_skill(self, skill):
        if skill["DefaultSkills"] == 1:
            return
        return False

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
        self.atkTargetsCount = [len(_["enemies_in_range"]) for _ in data]

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

        # exclusive类型 TODO #####
        print(f"atk_target: {score}")

        return score

    def atk_type(self, skill):
        # 选择攻击方式
        score = 0
        atk_type = self.strategy_params["atk_type"]
        if "skill" in atk_type:
            _score = 0 if self.is_default_skill(skill) else 1
            score += _score * atk_type["skill"][WEIGHT]

        if "normal" in atk_type:
            _score = 1 if self.is_default_skill(skill) else 0
            score += _score * atk_type["normal"][WEIGHT]

        # exclusive类型 TODO #####
        # exclusive类型 TODO #####
        print(f"atk_type: {score}")

        return score

    def move_position(self, atk_step):
        score = 0
        atk_targets = atk_step["enemies_in_range"]  # 攻击到的敌人list
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
        print(f"move_position: {score}")
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
        print(f"move_path: {score}")
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

        for each in atk_data:
            print("---------------------")
            _weight = 0
            skill = each["skill"]
            move_path = each["route"]
            enemies = each["enemies_in_range"]

            if "atk_target" in self.strategy_params:
                for e in enemies:
                    _weight += self.atk_target(e)

            # if "atk_type" in self.strategy_params:
            #     _weight += self.atk_type(skill)
            #
            # if "move_position" in self.strategy_params:
            #     _weight += self.move_position(each)
            #
            # if "move_path" in self.strategy_params:
            #     _weight += self.move_path(move_path)

            print(f"_weight: {_weight}")
            if _weight > weight:  # 筛选出权重最大的
                pick_data = each

        return pick_data


if __name__ == '__main__':
    tmp = "2024-08-28 15:57:03"

    tmp_data = eval(log_manager.get_log(tmp))
    print(tmp_data.keys())

    state = tmp_data["state"]
    role = tmp_data["role"]

    r = Range(role, state)
    data = [{}]
    f = ActionWeight(2, r.role, r.teammates, r.enemies)

    f.select_attack_strategy(data)
