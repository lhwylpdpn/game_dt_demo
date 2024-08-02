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
        self.__use_count = 999999999
        self.__max_use_count = self.__use_count
        self.fields = ["SkillId", "SkillLev", "DefaultSkills", "ActiveSkills", "effects", "use_count", "max_use_count"]

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
    
    def avaliable_effects(self): # 当前skill有哪些效果
        return [each.key for each in self.__effects]
    
    def get_effect_by_key(self, key):
        for each in self.__effects:
            if each.key == key:
                return each
        raise Exception(f"ERROR: {key} not exit in skill {self.skillId}")
    
    @property
    def use_count(self):
        return self.__use_count

    @property
    def max_use_count(self):
        return self.__use_count

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
        if new_effect.key == "USE_COUNT":
            self.__use_count = new_effect.param[0]
            self.__max_use_count = self.__use_count
        return self
    
    def use_skill(self): # 技能使用一次
        self.__use_count = self.__use_count - 1
        for each in self.__effects:
            if each.key == "USE_COUNT":
                each.param[0] = each.param[0] - 1
        return self

    def is_avaliable(self): # 判断技能是否可用
        return self.__use_count > 0

    
        
        