# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/21 16:15

class Data(object):
    @staticmethod
    def value(key: str, data: dict):
        if key in ("position", ):
            return tuple(data["position"])
        elif key in ("RoundAction", "DogBase"):
            return int(data[key])
        elif key in ("JumpHeight", ):
            return int(data[key][0])
        elif key in ("ClassType1", "ClassType2", "ClassType3", "ClassType4"):
            return int(data["BaseClass"][key])
        elif key in ("team_id", ):
            return data["team"][key]

        elif key in ("skills", "HeroID", "Hp", "HpBase", "Quality"):
            return data[key]
        else:
            raise Exception(f"Key Error! key={key}")

    @staticmethod
    def convert_maps_xz(maps):
        xz_dict = {}
        for k, v in maps.items():
            v["y"] = k[1]
            v["position"] = tuple(v["position"])
            xz_dict[(k[0], k[2])] = v
        return xz_dict

    @staticmethod
    def get_maps_point(xz, maps):
        y = maps[xz]["y"]
        return xz[0], y, xz[1]

    @staticmethod
    def intersection(list1, list2):
        # 返回并集
        return set(list1) & set(list2)

    @staticmethod
    def block_score(point_data):
        if point_data["Block"] == 0:
            return 1000
        if point_data["Block"] == 1:
            return 1
        if point_data["Block"] == 2:
            return 3
        if point_data["Block"] == 3:
            return 5

    @staticmethod
    def get_xz(point):
        return point[0], point[2]