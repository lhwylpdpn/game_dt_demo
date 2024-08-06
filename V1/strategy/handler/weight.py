# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/1 15:59
import math


class Weight(object):

    def health_weight(self, current_health, max_health):
        # /辅助类技能权重加总/血量权重
        if current_health <= 0 or max_health <= 0:
            raise ValueError("当前血量和最大血量必须>0！")
        if current_health > max_health:
            raise ValueError("current_health > max_health!")

        _ratio = float(current_health / max_health)
        if _ratio >= 0.95:
            return -1000  # 当剩余血量比率>=0.95，权重设为-1000
        value = 1 - math.log(_ratio) / math.log(1.01)
        return int(value)

    def attack_skill_weight(self, enemies):
        # /攻击类技能权重
        _weight = 0
        # 逻辑# TODO： AI类型=攻击型，攻击技能权重 = 100
        _weight += len(enemies) * 10  # 能攻击到的敌人数量：数量x10

        for e in enemies:
            _weight += int((1 - e["Hp"] / e["HpBase"]) * 10)
        # 逻辑# TODO：包括连击 / 连携
        return _weight

    def target_distance_weight(self, route):
        """ 目标距离权重 """
        return (len(route) - 1) * -5

    def remain_attack_use_weight(self, skill):
        """ 攻击的剩余使用次数权重 """
        _weight = 0
        # TODO 判断是否为普攻
        if skill["DefaultSkills"] == 1:
            _weight = 10
            return _weight

        _weight += int((int(skill["use_count"]) / int(skill["max_use_count"])) * 10)
        return _weight

    def target_weight(self, enemies):
        """ 目标类型权重 """
        # TODO
        pass

    def movement_strategy_weight(self, ai, target):
        if ai == "占据制高点":
            pass

    def atk_enemies_count_weight(self, enemies):
        return len(enemies) * 5

    def clac_move_target_weight(self, data):
        enemies = data["enemies_in_range"]

        atk_enemies_count_weight = self.atk_enemies_count_weight(enemies)
        weight = atk_enemies_count_weight
        return weight

    def clac_skill_weight(self, data):
        skill = data["skill"]
        enemies = data["enemies_in_range"]
        route = data["route"]

        attack_skill_weight = self.attack_skill_weight(enemies)
        remain_attack_use_weight = self.remain_attack_use_weight(skill)
        target_distance_weight = self.target_distance_weight(route)

        weight = attack_skill_weight + remain_attack_use_weight + target_distance_weight
        return weight


if __name__ == '__main__':
    f = Weight()
