# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/19 17:10

class DictUtils(object):
    @staticmethod
    def value(key: str, data: dict):
        if key in ("position", ):
            return tuple(data["position"])
        elif key in ("RoundAction", "DogBase"):
            return int(data[key])
        elif key in ("JumpHeight", ):
            return int(data[key][0])

        elif key in ("skills", "HeroID", "Hp", "HpBase"):
            return data[key]
        else:
            raise Exception(f"Key Error! key={key}")

