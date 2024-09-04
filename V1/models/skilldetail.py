# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-22
"""
import copy
from utils.tools import random_choices

class SkillDetail():
    
    def __init__(self, **kwargs):
        self.__SkillId = kwargs.get("SkillId", None)
        self.__SkillLev = kwargs.get("SkillLev", None)
        self.__DefaultSkills = kwargs.get("DefaultSkills", None)   # 0，1 1代表默认，即普通攻击
        self.__ActiveSkills	= kwargs.get("ActiveSkills", 0)        # 0，1  1 主动技能，0被动技能
        self.__SkillGoals = kwargs.get("SkillGoals", [])           # 1敌人  2地格  3自身  4友方
        self.__effects = []
        self.__use_count = None
        self.__max_use_count = self.__use_count
        self.fields = ["SkillId", "SkillLev", "DefaultSkills", "ActiveSkills", "SkillGoals", "effects", "max_use_count", "use_count"]
        #self.fields = ["SkillId", "SkillLev", "DefaultSkills", "ActiveSkills", "effects", "max_use_count"]

    def dict(self, fields=[], for_view=False, **kwargs):
        if not fields:
            fields = copy.deepcopy(self.fields)
        data = {}
        if "effects" in fields:
            data["effects"] = {}
            fields.remove("effects")
            for each in self.__effects:
                data["effects"][each.key] = each.dict()
        data.update({field:self.__getattribute__(field) for field in fields})
        if for_view:
            data.pop("max_use_count")
            data.pop("use_count")
        return data
    
    def avaliable_effects(self): # 当前skill有哪些效果
        return [each.key for each in self.__effects]
    
    def get_effect_by_key(self, key):
        for each in self.__effects:
            if each.key == key:
                return each
        print(f"Warn: {key} not exit in skill {self.SkillId}, so return None")
        return None
    
    @property
    def use_count(self):
        return self.__use_count

    @property
    def max_use_count(self):
        return self.__max_use_count

    @property
    def SkillId(self):
        return self.__SkillId
    
    def set_SkillId(self, v):
        self.__SkillId = v
        return self
    
    @property
    def SkillGoals(self):
        return self.__SkillGoals
    
    def set_SkillGoals(self, v):
        self.__SkillGoals = v
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
    
    def is_active_skill(self): #是否是主动技能
        return int(self.ActiveSkills) == 1
    
    @property
    def effects(self):
        return self.__effects
    
    def set_effects(self, v):
        self.__effects = v
        return self
    
    def effects_add(self, new_effect):
        self.__effects.append(new_effect)
        # 技能按照优先级排序
        self.__effects = sorted(self.__effects, key=lambda x:x.Priority, reverse=True) 
        if new_effect.key == "USE_COUNT":
            self.__use_count = int(new_effect.param[0])
            self.__max_use_count = self.__use_count
        return self
    
    def use_skill(self, hero_or_monster): # 技能使用一次
        for each in self.__effects:
            if each.key == "USE_COUNT":
                self.__use_count = self.__use_count - 1
                each.param[0] = str(int(each.param[0]) - 1)
        self.make_invalid(hero_or_monster)
        return self

    def is_avaliable(self): # 判断技能是否可用
        if self.__use_count is None:
            return True
        else:
            return self.__use_count > 0 
    
    def is_default_skill(self):
        return self.__DefaultSkills == 1
    
    def is_buff(self): # BUFF: 非主动，非被动触发的技能, 不是被普通攻击 , 不是连携, 不是被普攻时候出发
        if  not self.is_active_skill() and\
            "IS_HIT" not in self.avaliable_effects() and\
            "IS_SKILL_HIT" not in self.avaliable_effects() and\
            "IS_WAIT" not in self.avaliable_effects() and\
            "IS_NEAR_HERO" not in self.avaliable_effects() and\
            "IS_DEFAULT_HIT" not in self.avaliable_effects():
            return True
        return False
    
    def is_unit_skill(self): # BUFF: 非主动，非被动触发的技能, 不是被普通攻击 , 是连携, 不是被普攻时候出发
        if  not self.is_active_skill() and\
            "IS_HIT" not in each_skill.avaliable_effects() and\
            "IS_WAIT" not in each_skill.avaliable_effects() and\
            "IS_NEAR_HERO" in each_skill.avaliable_effects() and\
            "IS_DEFAULT_HIT" not in each_skill.avaliable_effects():
            return True
        return False
        
    def make_effective(self, hero_or_monster): # 生效
        for each in self.effects:
            if each.key in ['ADD_HP', 'ADD_DEF', 'ADD_MAGICAL_DEF', 'ADD_ATK',]:
                each.set_random(random_choices({True:int(each.param[0])/100.0, False:1 - int(each.param[0])/100.0}))
                if each.random: # 几率判断
                    if each.key == "ADD_HP": # 血是恢复 {0}%机率回复体力上限的{0}%
                        hp = hero_or_monster.Hp +  hero_or_monster.HpBase * int(each.param[1])/100.0
                        hero_or_monster.set_Hp(hero_or_monster.HpBase if hp >= hero_or_monster.HpBase else hp)
                    elif each.key == "ADD_DEF": # 
                        hero_or_monster.set_Def(hero_or_monster.Def + hero_or_monster.DefBase * (1 + int(each.param[1])/100.0))
                    elif each.key == "ADD_MAGICAL_DEF": # 
                        hero_or_monster.set_MagicalDef(hero_or_monster.MagicalDef + hero_or_monster.MagicalDefBase * (1 + int(each.param[1])/100.0))
                    elif each.key == "ADD_ATK": #
                        hero_or_monster.set_Atk(hero_or_monster.Atk + hero_or_monster.AtkBase * (1 + int(each.param[1])/100.0))
                    else:
                        pass
            else:
                continue
        return hero_or_monster
    
    def make_invalid(self, hero_or_monster): # 失效
        for each in self.effects:
            if each.key in ['ADD_HP', 'ADD_DEF', 'ADD_MAGICAL_DEF', 'ADD_ATK',]:
                if each.random :# 几率判断
                    if each.key == "ADD_HP": # 血是恢复 {0}%机率回复体力上限的{0}%
                        pass
                    elif each.key == "ADD_DEF": # 
                        hero_or_monster.set_Def(hero_or_monster.Def - hero_or_monster.DefBase * int(each.param[1])/100.0)
                    elif each.key == "ADD_MAGICAL_DEF": # 
                        hero_or_monster.set_MagicalDef(hero_or_monster.MagicalDef - hero_or_monster.MagicalDefBase * int(each.param[1])/100.0)
                    elif each.key == "ADD_ATK": #
                        hero_or_monster.set_Atk(hero_or_monster.Atk - hero_or_monster.AtkBase * int(each.param[1])/100.0)
                    else:
                        pass
                each.set_random(None)
            else:
                continue
        return hero_or_monster
        
    
        
        