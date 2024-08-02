# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-18
"""

import pandas as pd
import numpy as np
from utils.transposition import trans_postion


class Map(): # 地图
    """
    
    """
    def __init__(self, x, y, z): # 进来的参数是 地图的xyz，世界坐标的xzy
        self.size = trans_postion(x, y, z)
        self.map = np.zeros(self.size, dtype=np.object)

    def view_from_z(self):
        return np.max(self.map, axis=2)
    
    def dict(self):
        data = []
        for each_postion in self.list_land_postion():
            x,y,z = each_postion
            land = self.map[x,y,z]
            if isinstance(land, Land):
                data.append(land.dict())
        return data
    
    def load_land(self,x,y,z, land): # 加载地块
        x,y,z = trans_postion(x,y,z)
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
        


class Land(): # 地块
    
    def __init__(self, **kwargs):
        self.__position = list(trans_postion(*kwargs.get("position", None)))
        self.__sn = kwargs.get("sn", None)
        self.__PlotDescription = kwargs.get("PlotDescription", None)
        self.__Ap = kwargs.get("Ap", None)
        self.__Block = kwargs.get("Block", None)
        self.__DestroyEffectsId = kwargs.get("DestroyEffectsId", [])
        self.__DestroyState = kwargs.get("DestroyState", [])
        self.__DestroyHp = kwargs.get("DestroyHp", None)
        self.__effects = kwargs.get("effects", [])
    
    def dict(self, fields=[]):
        fields = ["position", "sn", "PlotDescription", "Ap", "Block", "DestroyEffectsId", "DestroyState", "DestroyHp", "effects"]
        data = {field: self.__getattribute__(field) for field in fields}
        return data
    
    def __gt__(self, other):
        if isinstance(other, Land):
            other = other.position[1]
        if self.position[1] > other:
            return True
        return False
    
    def __lt__(self, other):
        if isinstance(other, Land):
            other = other.position[1]
        if self.position[1] < other:
            return True
        return False
    
    def __le__(self, other):
        if isinstance(other, Land):
            other = other.position[1]
        if self.position[1] <= other:
            return True
        return False
    
    def __ge__(self, other):
        if isinstance(other, Land):
            other = other.position[1]
        if self.position[1] >= other:
            return True
        return False
    
    def __eq__(self, other):
        if isinstance(other, Land):
            other = other.position[1]
        if self.position[2] == other:
            return True
        return False
        
    @property
    def position(self): # 
        return self.__position
    
    def set_position(self, position):
        self.__position = position
        return self 
    
    
    @property
    def sn(self): # 
        return self.__sn
    
    def set_sn(self, sn_new):
        self.__sn = sn_new
        return self 
    
    @property
    def PlotDescription(self): # 
        return self.__PlotDescription
    
    def set_PlotDescription(self, v):
        self.__PlotDescription = v
        return self
    
    @property
    def Ap(self): # 
        return self.__Ap
    
    def set_Ap(self, v):
        self.__Ap = v
        return self 
    
    @property
    def Block(self): # 
        return self.__Block
    
    def set_Block(self, v):
        self.__Block = v
        return self 
    
    @property
    def DestroyEffectsId(self): # 
        return self.__DestroyEffectsId
    
    def set_DestroyEffectsId(self, v):
        self.__DestroyEffectsId = v
        return self
    
    @property
    def DestroyState(self): # 
        return self.__DestroyState
    
    def set_DestroyState(self, v):
        self.__DestroyState = v
        return self
    
    @property
    def DestroyHp(self): # 
        return self.__DestroyHp
    
    def set_DestroyHp(self, v):
        self.__DestroyHp = v
        return self
    
    @property
    def effects(self): # 
        return self.__effects
    
    def set_effects(self, v):
        self.__effects = v
        return self
            

if __name__ == "__main__":
   print(Map(4,4,4).view_from_y())