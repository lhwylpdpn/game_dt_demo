# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-18
"""

import pandas as pd
import numpy as np


class Map(): # 地图
    def __init__(self, x, y, z):
        self.size = [x, y, z]
        self.map = np.zeros((x, y, z), dtype=np.object)
        # self.map[0,0,0] = Land()
        # self.map[0,1,0] = Land()
        # self.map[0,2,0] = Land()
        # self.map[0,0,1] = Land()
        # print(self.map)
        # print("****************")
    
    def view_from_y(self):
        return np.max(self.map, axis=1)
    
    def load_land(self,x,y,z, land): # 加载地块
        self.map[x,y,z] = land
        return self
    
    @staticmethod
    def find_map_size(origin_map_data):
        postion_list = []
        for each in origin_map_data:
            postion_list.append(each.get('position'))
        df = pd.DataFrame(postion_list)
        return list(df.max())


class Land(): # 地块
    
    def __init__(self, **kwargs):
        self.__sn = kwargs.get("sn", None)
        self.__PlotDescription = kwargs.get("PlotDescription", None)
        self.__Ap = kwargs.get("Ap", None)
        self.__Block = kwargs.get("Block", None)
        self.__DestroyEffectsId = kwargs.get("DestroyEffectsId", [])
        self.__DestroyState = kwargs.get("DestroyState", [])
        self.__DestroyHp = kwargs.get("DestroyHp", None)
        self.__effects = kwargs.get("effects", [])
    
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