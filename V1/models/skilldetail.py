# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-22
"""
import copy
from utils.tools import random_choices
from collections import namedtuple

SKILL_DEFAULT = namedtuple("SKILL_DEFAULT", ['NORMAL', 'DEFAULT'])
skill_default = SKILL_DEFAULT(0, 1)

SKILL_GOALS = namedtuple("SKILL_GOALS", ['ENEMY','LAND','SELF', 'FRIENDS'])
skill_goals = SKILL_GOALS(1, 2, 3, 4)

SKILL_CLASS = namedtuple("SKILL_CLASS", ['ACTIVE', 'SUPPORT', 'MOVE', 'BACK'])
skill_class = SKILL_CLASS(1, 2, 3, 4)

SKILL_CALC = namedtuple("SKILL_CALC", ['NA', 'ATTACK', 'HALO', 'TRIGGER', 'OUT', 'TREATMENT', 'SETTLEMENT'])
skill_calc = SKILL_CALC(0, 1, 2, 3, 4, 5, 6)

SKILL_ELEMENT = namedtuple("SKILL_ELEMENT", ['NA', 'WATER', 'FIRE', 'EARTH', 'MUDD', 'LIGHT', 'DARK', 'PHYSIC'])
skill_element = SKILL_ELEMENT(0, 1, 2, 3, 4, 5, 6, 7)


class SkillDetail():
    
    def __init__(self, **kwargs):
        self.__SkillId = kwargs.get("SkillId", None)
        self.__SkillLev = kwargs.get("SkillLev", None)
        self.__DefaultSkills = kwargs.get("DefaultSkills", None)   # 0，1 1代表默认，即普通攻击
        self.__SkillClass = kwargs.get("SkillClass", None)         # 技能类别 1:主动技能 2:支援技能 3:移动技能 4:反应技能
        self.__SkillCalc = kwargs.get("SkillCalc", 0)              # 计算类别 0: 无， 1:攻击， 2:光环， 3:触发， 4:局外，5:治疗 6:结算
        self.__SkillElement = kwargs.get("SkillElement", 0)        # 元素属性 0:无， 1:水， 2:火，3:地， 4:木，5:光，6:暗， 7:物理
        self.__SkillGoals =[int(_) for _ in kwargs.get("SkillGoals", [])]       #技能目标  1敌人  2地格  3自身  4友方
        
        self.__effects = []
        self.__use_count = None
        self.__max_use_count = self.__use_count
        self.fields = ["SkillId", "SkillLev", "DefaultSkills", "SkillClass",  "SkillCalc",  "SkillElement",
                        "SkillGoals", "effects", "max_use_count", "use_count"]

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
    
    # 是单体技能还是攻击技能
    
    @property
    def use_count(self):
        if self.__use_count is None:
            return -1
        return self.__use_count

    @property
    def max_use_count(self):
        if self.__max_use_count is None:
            return -1
        return self.__max_use_count
 
    @property
    def SkillId(self):
        return self.__SkillId
    
    def set_SkillId(self, v):
        self.__SkillId = v
        return self

    @property
    def SkillClass(self):
        return self.__SkillClass
    
    def set_SkillClass(self, v):
        self.__SkillClass = v
        return self
    
    @property
    def SkillCalc(self):
        return self.__SkillCalc
    
    def set_SkillCalc(self, v):
        self.__SkillCalc = v
        return self

    @property
    def SkillElement(self):
        return self.__SkillElement
    
    def set_SkillElement(self, v):
        self.__SkillElement = v
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
        if self.__use_count is None or self.__use_count == -1:
            return True
        else:
            return self.__use_count > 0 
    
    def is_default_skill(self):
        return self.__DefaultSkills == skill_default.DEFAULT

    def is_active_skill(self):
        return self.__SkillClass == skill_class.ACTIVE
    
    def is_medical_skill(self): # 是否是治疗技能
        return self.__SkillCalc == skill_calc.TREATMENT

    def is_move_skill(self): # 是否是移动技能
        return self.__SkillClass == skill_class.MOVE
    
    def is_dont_move_media_self_skill(self): # 是否是不移动技能, 治疗自己技能
        if self.__SkillClass == skill_class.MOVE and self.__SkillCalc == skill_calc.TRIGGER:
            if [skill_goals.SELF] == self.SkillGoals: # 起作用的只是自己
                return True
        return False
    
    def is_back_NA_skill(self): # 反应技能（加属性的）
        # 反应技能，技能类型是 TRIGGER
        if self.__SkillClass == skill_class.BACK and self.__SkillCalc == skill_calc.TRIGGER:
            if [skill_goals.SELF] == self.SkillGoals: # 起作用的只是自己
                return True
        return False

    def is_back_attack_skill(self): # 被动反击技能
        # 反应技能，技能类型是 TRIGGER
        if self.__SkillClass == skill_class.BACK and self.__SkillCalc == skill_calc.TRIGGER:
            if skill_goals.ENEMY in self.SkillGoals: # 起作用的是敌人
                return True
        return False
    
    def is_default_hit(self): # 反应技能，默认技能攻击时候触发
        return "IS_DEFAULT_HIT" in self.avaliable_effects()
    
    def is_hit(self):  # 反应技能，被攻击时候触发
        return "IS_HIT"  in self.avaliable_effects()

    def is_skill_hit(self):  # 反应技能，被技能攻击时候触发
        return "IS_SKILL_HIT"  in self.avaliable_effects()

    def is_miss_damage(self):
        return "MISS_DAMAGE" in self.avaliable_effects()
    
    def is_active_attack_skill(self): # 主动攻击技能
        return self.__SkillClass == skill_class.ACTIVE and self.__SkillCalc == skill_calc.ATTACK
    
    def is_buff(self): # BUFF: 非主动，非被动触发的技能, 不是被普通攻击 , 不是连携, 不是被普攻时候出发
        if  not self.is_active_skill() and\
            "IS_VICTORY" not in self.avaliable_effects() and\
            "IS_HIT" not in self.avaliable_effects() and\
            "IS_SKILL_HIT" not in self.avaliable_effects() and\
            "IS_WAIT" not in self.avaliable_effects() and\
            "IS_NEAR_HERO" not in self.avaliable_effects() and\
            "IS_DEFAULT_HIT" not in self.avaliable_effects():
            return True
        return False
    
    def is_unit_skill(self): # BUFF: 非主动，非被动触发的技能, 不是被普通攻击 , 是连携, 不是被普攻时候出发
        if  not self.is_active_skill() and\
            "IS_HIT" not in self.avaliable_effects() and\
            "IS_WAIT" not in self.avaliable_effects() and\
            "IS_NEAR_HERO" in self.avaliable_effects() and\
            "IS_DEFAULT_HIT" not in self.avaliable_effects():
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
                        hero_or_monster.set_Def(hero_or_monster.Def + hero_or_monster.DefBase *  + int(each.param[1])/100.0)
                    elif each.key == "ADD_MAGICAL_DEF": # 
                        hero_or_monster.set_MagicalDef(hero_or_monster.MagicalDef + hero_or_monster.MagicalDefBase *  int(each.param[1])/100.0)
                    elif each.key == "ADD_ATK": #
                        hero_or_monster.set_Atk(hero_or_monster.Atk + hero_or_monster.AtkBase * int(each.param[1])/100.0)
                    else:
                        pass
            elif each.key in ['ADD_VELOCITY', 'ADD_JUMP_HEIGHT', 'ADD_HP_FORMULA_1', 'ADD_HP_FORMULA_2',
                              'ADD_TEAM_ROLE_EXP', 'ADD_TEAM_BASE_EXP', 'ADD_ROUND_ACTION', "ADD_ROLE_EXP"]:
                if each.key == "ADD_VELOCITY":#
                    hero_or_monster.set_Velocity(hero_or_monster.Velocity + each.param[0])
                elif each.key == "ADD_HP_FORMULA_1":#
                    hp = hero_or_monster.Hp +  hero_or_monster.MagicalAtkBase * int(each.param[0])/100.0
                    hero_or_monster.set_Hp(hero_or_monster.HpBase if hp >= hero_or_monster.HpBase else hp)
                elif each.key == "ADD_HP_FORMULA_2":#
                    hp = hero_or_monster.Hp +  hero_or_monster.HpBase * int(each.param[0])/100.0
                    hero_or_monster.set_Hp(hero_or_monster.HpBase if hp >= hero_or_monster.HpBase else hp)
                elif each.key == "ADD_JUMP_HEIGHT":#
                    hero_or_monster.set_JumpHeight(list(map(lambda x: x + each.param[0], hero_or_monster.JumpHeight)))
                elif each.key == "ADD_TEAM_ROLE_EXP":#
                    print("ADD_TEAM_ROLE_EXP: 没有Exp，暂时不实现")
                elif each.key == "ADD_TEAM_BASE_EXP":#
                    print("ADD_TEAM_BASE_EXP: 没有Exp，暂时不实现") 
                elif each.key == "ADD_ROLE_EXP":#
                    print("ADD_ROLE_EXP: 没有Exp，暂时不实现") 
                elif each.key == "ADD_ROUND_ACTION":#
                    hero_or_monster.set_RoundAction(hero_or_monster.RoundAction + each.param[0])
                else:
                    pass
            elif each.key in ['REMOVE_DEBUFF']:
                if each.key == "REMOVE_DEBUFF":#
                    hero_or_monster.remove_debuff()        
            else:
                continue
        return hero_or_monster
    
    def make_invalid(self, hero_or_monster): # 失效
        for each in self.effects:
            if each.key in ['ADD_DEF', 'ADD_MAGICAL_DEF', 'ADD_ATK',]:
                if each.random :# 几率判断
                    if each.key == "ADD_DEF": # 
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
        
    
        
        