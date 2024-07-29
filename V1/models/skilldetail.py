# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-22
"""


class SkillDetail():
    
    def __init__(self, **kwargs):
        self.__sn = kwargs.get("sn", None)	
        self.__SkillId = kwargs.get("SkillId", None)
        self.__SkillLev = kwargs.get("SkillLev", None)
        self.__desc = kwargs.get("desc", None)
        self.__SkillIcon = kwargs.get("SkillIcon", None)
        self.__SkillSpine	= kwargs.get("SkillSpine", None)
        self.__effecDescribe	= kwargs.get("effecDescribe", None)
        self.__skill_type = kwargs.get("skill_type", None)
        self.__range = kwargs.get("range", None)
        self.__effects = []
        self.init_data = kwargs
    
    def dict(self, fields=[]):
        if not fields:
            fields = list(self.init_data.keys())
        data = {}
        if "effects" in fields:
            data["effects"] = []
            fields.remove("effects")
            for each in self.__effects:
                data["effects"].append(each.dict())
        data.update({field:self.__getattribute__(field) for field in fields})
        return data
    
    @property
    def sn(self):
        return self.__sn
    
    def set_sn(self, v):
        self.__sn = v
        return self
    
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
    def desc(self):
        return self.__desc
    
    def set_desc(self, v):
        self.__desc = v
        return self
    
    @property
    def SkillIcon(self):
        return self.__SkillIcon
    
    def set_SkillIcon(self, v):
        self.__SkillIcon = v
        return self
    
    @property
    def SkillSpine(self):
        return self.__SkillSpine
    
    def set_SkillSpine(self, v):
        self.__SkillSpine = v
        return self
    
    @property
    def effecDescribe(self):
        return self.__effecDescribe
    
    def set_effecDescribe(self, v):
        self.__effecDescribe = v
        return self

    @property
    def skill_type(self):
        return self.__skill_type
    
    def set_skill_type(self, v):
        self.__skill_type = v
        return self

    @property
    def range(self):
        return self.__range
    
    def set_range(self, v):
        self.__range = v
        return self
    
    @property
    def effects(self):
        return self.__effects
    
    def set_effects(self, v):
        self.__effects = v
        return self
    
    def effects_add(self, new_effect):
        self.__effects.append(new_effect)
        return self
