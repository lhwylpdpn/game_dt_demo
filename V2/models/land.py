# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-14
"""

HEIGHT = 1     # 1 y轴， 2 Z轴
CAN_PASS = 0

class LandBase(): # 地块基础数据
    
    def __init__(self, **kwargs):
        self.__position = kwargs.get("position", None)                        # 坐标
        self.__sn = kwargs.get("sn", None)                                    # sn
        self.__Block = kwargs.get("Block", CAN_PASS)                          # 收否可以通过 0可以，其他不可以
        self.__Block_Base = kwargs.get("Block", CAN_PASS)                     # 收否可以通过 0可以，其他不可以
        # self.__Selected = kwargs.get("Selected", 0)                           # 是否可以被攻击
        # self.__layer2 = kwargs.get("layer2", None)                            # 地块上的附着物
        # self.__layer3 = kwargs.get("layer3", None)                            # 地块上的附着物
        # self.__layer4 = kwargs.get("layer4", None)                            # 地块上的附着物
        self.__stand_object = None                                            # 地块上站立的对象
    
    def dict(self):
        #fields = ["sn", "Block", "Block_Base", "Selected", "position"]
        fields = ["sn", "Block", "Block_Base", "position"]
        #fields = [_.replace("__", "") for _ in  self.__dict__.keys()]
        return {_:self.__getattribute__(_) for _ in fields}
    
    def __gt__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] > other:
            return True
        return False
    
    def __lt__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] < other:
            return True
        return False
    
    def __le__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] <= other:
            return True
        return False
    
    def __ge__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] >= other:
            return True
        return False
    
    def __eq__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] == other:
            return True
        return False
    
    @property
    def sn(self):
        return self.__sn
    
    @property
    def Block(self):
        return self.__Block
    
    def set_Block(self, nb):
        self.__Block = nb
        return self
    
    @property
    def Block_Base(self):
        return self.__Block_Base
    
    @property
    def Selected(self):
        return self.__Selected
    
    @property
    def position(self):
        return self.__position
    
    @property
    def stand_object(self): 
        return self.__stand_object
    
    def set_stand_object(self, v):
        self.__stand_object = v
        self.set_Block()    
        return self
    
    def set_Block(self):
        if self.__stand_object: # 站立了英雄ormonster
            self.__Block = self.__stand_object.Block
        else:
            self.block = self.Block_Base
        return self

class Land(LandBase):
    
    def __init__(self, **kwargs):
        super(Land, self).__init__(**kwargs)
    
    def dict(self):
        dict_data = super().dict()
        return dict_data
    
    def is_can_pass(self):
        return self.Block == CAN_PASS
    
 