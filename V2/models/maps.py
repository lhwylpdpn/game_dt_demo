# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-18
"""

import pandas as pd
import copy
import numpy as np
import itertools
from .land import Land


class Map(): # 地图
    """
    """
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
        self.map = np.zeros((self._x, self._y, self._z), dtype=np.object)
    
    @staticmethod
    def build_map(origin_map_data):  # 返回加载地块的MAP对象
        map = Map(*Map.find_map_size(origin_map_data))
        for each in origin_map_data:
            position = each.get("position")
            land = Land(**each)
            map.load_land(*position, land)
        return map

    @property
    def x(self):
        return self._x - 1
    
    @property
    def y(self):
        return self._y - 1
    
    @property
    def z(self):
        return self._z - 1
    
    def view_from_y(self):
        return np.max(self.map, axis=1)
    
    def correct_map_bonus(self, x, z): # x, z 中检查地图的边界
        x = x if self.x > x else self.x
        x = 0 if x < 0 else  x
        z = z if self.z > z  else  self.z
        z = 0 if z < 0 else z
        return x, z

    def get_y_from_xz(self, x, z):  # 从y俯视图中，根据 x,z 来确定 地块
        if x >=0 and x <= self.x and z >= 0 and z <= self.z:
            position = np.max(self.map[x, :, z], axis=0)
            if isinstance(position, Land):
                return position.y
            else:
                return None
        else:
            raise Exception(f"{x}, {z} is wrong")

    def land_can_pass(self, x, y, z): # 判断地图是否可以通过
        try:
            land = self.map[x,y,z]
            if isinstance(land, Land):
                if land.Block is None:
                    return False
                return land.is_can_pass()
            return False
        except Exception:
            return False
    
    def get_land(self, x, y, z):  # 获取地图上的地块
        try:
            land = self.map[x,y,z]
            if isinstance(land, Land):
                return land
            return None
        except Exception:
            return None

    def view_from_y_dict(self):
        data = {}
        a = pd.DataFrame(self.view_from_y())
        for each_coloum in np.array(a.values.tolist()).tolist():
            for each in each_coloum:
                if isinstance(each, Land):
                    x,y,z = each.position
                    land = self.map[x,y,z]
                    data[(x,y,z)] = land.dict()
        return data

    def dict(self, for_view=False):
        data = []
        for each_postion in self.list_land_postion():
            x,y,z = each_postion
            land = self.map[x,y,z]
            if isinstance(land, Land):
                land_data = land.dict()
                data.append(land_data)
        return data
    
    def exit(self, h_m_object): # 离开地块
        x,y,z = h_m_object.position
        land = self.map[x,y,z]
        if isinstance(land, Land):
            if land.stand_object:
                if land.stand_object.HeroID == h_m_object.HeroID:
                    land.set_stand_object(None)
                else:
                    raise Exception("地块 {x}, {y}, {z} 不是该对象站立")
        return self
    
    def enter(self, x, y, z, h_m_object, init_position=False, **kwargs): # 进入地块 
        land = self.map[x,y,z]
        if isinstance(land, Land):
            if not land.stand_object:
                land.set_stand_object(h_m_object)
                # if init_position:
                #     self.__h_m_objects.append(h_m_object)
            else:
                raise Exception("land {x}, {y}, {z} 被占用")
        return self
    
    def load_land(self,x,y,z, land): # 加载地块
        self.map[x,y,z] = land
        return self
    
    @staticmethod
    def find_map_size(origin_map_data):
        postion_list = []
        for each in origin_map_data:
            postion_list.append(each.get('position'))
        df = pd.DataFrame(postion_list)
        x, y, z = list(df.max())
        print("map size:", x+1, z+1, y+1)
        return x+1, y+1, z+1 
    
    def list_land_postion(self):
        a = pd.DataFrame(np.nonzero(self.map))
        return np.array(a.T.values.tolist()).tolist()