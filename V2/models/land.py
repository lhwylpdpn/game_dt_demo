# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-14
"""


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
        fields = ["sn", "Block", "Block_Base", "Selected", "position"]
        return {_:self.__getattribute__(_) for _ in fields}
    
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


class Land(LandBase):
    
    def __init__(self, **kwargs):
        super(Land, self).__init__(**kwargs)
    
    def dict(self):
        dict_data = super().dict()
        return dict_data
    
    def is_can_pass(self):
        return self.Block == CAN_PASS
    
    @property
    def stand_object(self): 
        return self.__stand_object
    
    def set_stand_object(self, v):
        self.__stand_object = v
        self.set_Block()
        if self.__stand_object:
            for _ in self.attachments:
                self.add_buff_for_stand_object(_)       
        return self
    
    def set_Block(self):
        if self.__stand_object: # 站立了英雄ormonster
            self.__Block = self.__stand_object.Block
        else:
            block = self.Block_Base
        return self 