# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-06

"""
from utils.tools import uniqueID_32, uniqueID_64

class CardBase():
    
    def __init__(self, **kwargs):
        self.__CardID = kwargs.get("CardID", None)         # 卡牌ID
        self.__Cost = kwargs.get("Cost", None)             # 卡牌AP消耗值
        self.__Type = kwargs.get("Type", None)             # 卡牌类型  1 行动， 2 能力 3 召唤
        self.__AtkTarget = kwargs.get("AtkTarget", [])     # 卡牌攻击目标  1、地格 2、敌方 3、自身 3 友方
        self.__AtkDistance = kwargs.get("AtkDistance", []) # 卡牌攻击距离  行动 和召唤才有攻击距离
        self.__HitRange = kwargs.get("HitRange", [])       #  受击范围  
        self.__HitRangeType = kwargs.get("HitRangeType", None)         # 受击范围类型  1、菱形 2 正方形
        self.__Param = kwargs.get("Param", [])             # card effect 相关参数 ID|参数
        self.__releasePosition = None                         # 使用卡牌时候，卡牌的释放点位
                                   
    def dict(self):
        fields = ["CardID", "Cost", "Type", "AtkTarget", 
                 "AtkDistance", "HitRange", "HitRangeType", "Param", 'releasePosition']
        return {field:self.__getattribute__(field) for field in fields}
    
    ## attr
    @property
    def CardID(self):
        return self.__CardID
    
    @property
    def Cost(self):
        return self.__Cost
    
    @property
    def Type(self):
        return self.__Type
    
    @property
    def AtkTarget(self):
        return self.__AtkTarget
    
    @property
    def AtkDistance(self):
        return self.__AtkDistance
    
    @property
    def HitRange(self):
        return self.__HitRange
    
    @property
    def HitRangeType(self):
        return self.__HitRangeType
    
    @property
    def Param(self):
        return self.__Param 
    
    @property
    def releasePosition(self):
        return self.__releasePosition
    
    def set_releasePosition(self, value):
        self.__releasePosition = value
        return self
    

class Card(CardBase):

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.__effects = {}                  # 卡牌 的效果
        self.__unique_id = None
    
    def dict(self):
        dict_data = super().dict()
        dict_data["unique_id"] = self.unique_id
        dict_data["effects"] = {k:self.get_effect(k).dict() for k in self.effects.keys()}
        return dict_data
    
    def create_unique_id(self):
        self.__unique_id = uniqueID_32()
        return self
    
    @property
    def unique_id(self):
        return self.__unique_id

    @property
    def effects(self):
        return self.__effects
    
    def add_effect(self, effect):
        self.effects[effect.EffectID] = effect
        return self
    
    def get_effect(self, effect_id):
        return self.effects.get(effect_id, None)


