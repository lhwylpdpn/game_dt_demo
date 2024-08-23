# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/21 16:11
from utils.strategy_utils.basic_data import Data


class Clac(Data):

    def is_health_below_threshold(self, role, num):
        # 血量是否小于num比例
        if not isinstance(role, dict):
            role = role.dict()

        hp = Data.value("Hp", role)
        hp_base = Data.value("HpBase", role)
        return float(hp) / float(hp_base) < float(num)
