# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-22
"""
import copy

class SkillDetail():
    
    def __init__(self, **kwargs):
        self.__SkillId = kwargs.get("SkillId", None)
        self.__SkillLev = kwargs.get("SkillLev", None)
        self.__DefaultSkills = kwargs.get("DefaultSkills", None)   # 0，1 1代表默认，即普通攻击
        self.__ActiveSkills	= kwargs.get("ActiveSkills", None)     # 0，1  1 主动技能，0被动技能
        self.__effects = []
        self.__use_count = self.__use_count() # 使用次数限制
        self.fields = ["SkillId", "SkillLev", "DefaultSkills", "ActiveSkills", "effects"]

    def dict(self, fields=[]):
        if not fields:
            fields = copy.deepcopy(self.fields)
        data = {}
        if "effects" in fields:
            data["effects"] = {}
            fields.remove("effects")
            for each in self.__effects:
                data["effects"][each.key] = each.dict()
        data.update({field:self.__getattribute__(field) for field in fields})
        return data
    
    
    @property
    def SkillId(self):
        return self.__SkillId
    
    def set_SkillId(self, v):
        self.__SkillId = v
        return self
    
    @property
    def SkillLev(self):
        return self.__SkillLev
    
    def set_SkillLev(self, v):
        self.__SkillLev = v
        return self
    
    @property
    def DefaultSkills(self):
        return self.__DefaultSkills

    @property
    def ActiveSkills(self):
        return self.__ActiveSkills
    
    @property
    def effects(self):
        return self.__effects
    
    def set_effects(self, v):
        self.__effects = v
        return self
    
    def effects_add(self, new_effect):
        self.__effects.append(new_effect)
        return self

    def __use_count(self): # 加载使用次数限制，没有使用次数的时候，无限
        for each in self.__effects:
            if each.key == "USE_COUNT":
                c = each.param[0]
                return
        self.__use_count = 999999999
    
    def use_skill(self): # 技能使用一次
        self.__use_count = self.__use_count - 1
        return self

    def is_avaliable(self): # 判断技能是否可用
        if self.__use_count > 0

    
        
        