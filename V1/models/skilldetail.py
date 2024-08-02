# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-22
"""


class SkillDetail():
    
    def __init__(self, **kwargs):
        self.__SkillId = kwargs.get("SkillId", None)
        self.__SkillLev = kwargs.get("SkillLev", None)
        self.__DefaultSkills = kwargs.get("DefaultSkills", None)   # 0，1 1代表默认，即普通攻击
        self.__ActiveSkills	= kwargs.get("ActiveSkills", None)     # 0，1  1 主动技能，0被动技能
        self.__effects = []
        self.fields = ["SkillId", "SkillLev", "DefaultSkills", "ActiveSkills", "effects"]

    def dict(self, fields=[]):
        if not fields:
            fields = self.fields
        data = {}
        if "effects" in fields:
            data["effects"] = []
            fields.remove("effects")
            for each in self.__effects:
                data["effects"].append(each.dict())
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