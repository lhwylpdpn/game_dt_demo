# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-23
"""

class Carrer():
    
    def __init__(self, **kwargs):
        self.__sn = kwargs.get("sn", None)
        self.__classRank = kwargs.get("classRank", None)           # 职业品阶
        self.__name = kwargs.get("name", None)                     # 名称
        self.__preconditions = kwargs.get("preconditions", [])   # 前置条件
        self.__maleModel = kwargs.get("maleModel", None)           # 职业模型男
        self.__femaleModel = kwargs.get("femaleModel", None)       # 职业模型女
        self.__clazzIcon = kwargs.get("clazzIcon", None)           # 职业icon
        self.__primaryWeapon = kwargs.get("primaryWeapon", [])   # 初始武器·主
        self.__secondaryWeapons = kwargs.get("secondaryWeapons", []) # 初始武器·副
        self.__startingSkill = kwargs.get("startingSkill", [])     # 初始技能
        self.__upgradeType = kwargs.get("upgradeType", None)        # 升级方式
        self.__upgradeExp = kwargs.get("upgradeExp", None)          # 升级经验
        self.__maxGrade = kwargs.get("maxGrade", None)              # 最大等级
        self.__vocationalSkills = kwargs.get("vocationalSkills", []) # 职业技能
        self.__learningConsumption = kwargs.get("learningConsumption", []) # 学习消耗
        self.__openLevel = kwargs.get("openLevel", [])                   # 开放等级
        self.init_data = kwargs
    
    def dict(self, fields=[]):
        if fields:
            return {field:self.__getattribute__(field) for field in fields}
        else:
            return {field:self.__getattribute__(field) for field in self.init_data.keys()}
    
    @property    
    def sn(self):
        return self.__sn
    
    def set_sn(self, v):
        self.__sn = v
        return self
    
    @property    
    def classRank(self):
        return self.__classRank
    
    def set_classRank(self, v):
        self.__classRank = v
        return self
    
    @property    
    def name(self):
        return self.__name
    
    def set_name(self, v):
        self.__name = v
        return self

    @property    
    def preconditions(self):
        return self.__preconditions
    
    def set_preconditions(self, v):
        self.__preconditions = v
        return self
        
    @property    
    def maleModel(self):
        return self.__maleModel
    
    def set_maleModel(self, v):
        self.__maleModel = v
        return self
    
    @property    
    def femaleModel(self):
        return self.__femaleModel
        
    def set_femaleModel(self, v):
        self.__femaleModel = v
        return self
    
    @property    
    def clazzIcon(self):
        return self.__clazzIcon
        
    def set_clazzIcon(self, v):
        self.__clazzIcon = v
        return self
    
    @property    
    def primaryWeapon(self):
        return self.__primaryWeapon
        
    def set_primaryWeapon(self, v):
        self.__primaryWeapon = v
        return self
    
    @property    
    def secondaryWeapons(self):
        return self.__secondaryWeapons
        
    def set_secondaryWeapons(self, v):
        self.__secondaryWeapons = v
        return self
    
    @property    
    def startingSkill(self):
        return self.__startingSkill
        
    def set_startingSkill(self, v):
        self.__startingSkill = v
        return self
    
    @property    
    def upgradeType(self):
        return self.__upgradeType
        
    def set_upgradeType(self, v):
        self.__upgradeType = v
        return self
    
    @property    
    def upgradeExp(self):
        return self.__upgradeExp
        
    def set_upgradeExp(self, v):
        self.__upgradeExp = v
        return self
    
    @property    
    def maxGrade(self):
        return self.__maxGrade
        
    def set_maxGrade(self, v):
        self.__maxGrade = v
        return self
    
    @property    
    def vocationalSkills(self):
        return self.__vocationalSkills
        
    def set_vocationalSkills(self, v):
        self.__vocationalSkills = v
        return self
    
    @property    
    def learningConsumption(self):
        return self.__learningConsumption
        
    def set_learningConsumption(self, v):
        self.__learningConsumption = v
        return self
    
    @property    
    def openLevel(self):
        return self.__openLevel
        
    def set_openLevel(self, v):
        self.__openLevel = v
        return self
    
