# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-09-13
"""
import json
import copy

from collections import namedtuple


class BaseClass():
    
    def __init__(self, sn=None, Name=None, desc=None, 
                 ClassType1=None,  # 职业详细类别 前卫防守型 1 ； 后卫防守型 2
                 ClassType2=None,  # 位置类别    前卫      1  ； 后卫     2
                 ClassType3=None,  # 职能类别    防守      1  ； 攻击     2； 治疗 3
                 ClassType4=None,  # 攻击方式类别 近身持续输出 1； 远程输出 2； 近身爆发输出 3； 魔法输出 4； 治疗辅助 5
                 ClassType5=None,  # 预留
                 ClassType6=None,   # 预留
                 **kwargs):
        self.__sn = sn
        self.__Name = Name
        self.__desc = desc
        self.__ClassType1 = ClassType1
        self.__ClassType2 = ClassType2
        self.__ClassType3 = ClassType3
        self.__ClassType4 = ClassType4
        self.__ClassType5 = ClassType5
        self.__ClassType6 = ClassType6

        self.fields = ["sn", "Name", "desc", "ClassType1", "ClassType2", "ClassType3", "ClassType4"]
    
    def dict(self): 
        return {_:self.__getattribute__(_) for _ in self.__fields} 

    @property
    def sn(self):
        return self.__sn

    @property 
    def Name(self):
        return self.__Name

    @property
    def desc(self):
        return self.__desc

    @property
    def ClassType1(self):
        return self.__ClassType1

    @property
    def ClassType2(self):
        return self.__ClassType2

    @property
    def ClassType3(self):
        return self.__ClassType3

    @property
    def ClassType4(self):
        return self.__ClassType4
    
    @property
    def ClassType5(self):
        return self.__ClassType5

    @property
    def ClassType6(self):
        return self.__ClassType6