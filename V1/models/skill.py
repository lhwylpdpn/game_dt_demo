# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-22
"""

SKILL_DIC = {
    
} 


class Skill():

    def __init__(self, **kwargs): 
        """ sn=None, skillId=None, skillUser=None, equipPosition=None,
        skillType=[], defaultSkills=None, skillRank=None,
        activeSkills=None, skillGoals=[], skillName=None,
        breakoutName=None, skillDescription=None, skillIntroduce=None,
        parm1=[], parm2=[], parm3=[], parm4=[],
        savedPreset=None, skillPreset=None, hitPreset=None,
        ballisticsPreset=None, weaponPresets=None,
        spineAction=None,"""
        self.__sn = kwargs.get("sn", None)                              #sn
        self.__skillId = kwargs.get("skillId", None)                    #技能ID
        self.__skillUser = kwargs.get("skillUser", None)                #技能使用者
        self.__equipPosition = kwargs.get("equipPosition", None)        #对应装备位置
        self.__skillType = kwargs.get("skillType", [])                  #技能类型-对应主武器类型
        self.__defaultSkills = kwargs.get("defaultSkills", None)        #默认技能 0否1是
        self.__skillRank = kwargs.get("skillRank", None)                #技能品质
        self.__activeSkills = kwargs.get("activeSkills", None)          #主动技能
        self.__skillGoals = kwargs.get("skillGoals", [])                #技能目标
        self.__skillName = kwargs.get("skillName", None)                #技能名称
        self.__breakoutName = kwargs.get("breakoutName", None)          #突破名称
        self.__skillDescription = kwargs.get("skillDescription", None)  #技能描述
        self.__skillIntroduce = kwargs.get("skillIntroduce", None)      #技能介绍
        self.__parm1 = kwargs.get("parm1", [])                          #参数1
        self.__parm2 = kwargs.get("parm2", [])                          #参数2
        self.__parm3 = kwargs.get("parm3", [])                          #参数3
        self.__parm4 = kwargs.get("parm4", [])                          #参数4
        self.__savedPreset = kwargs.get("savedPreset", None)            #蓄力预置
        self.__skillPreset = kwargs.get("skillPreset", None)            #攻击预置
        self.__hitPreset = kwargs.get("hitPreset", None)                #受击预置
        self.__ballisticsPreset = kwargs.get("ballisticsPreset", None)  #弹道预置
        self.__weaponPresets = kwargs.get("weaponPresets", None)        #武器预置 
        self.__spineAction = kwargs.get("spineAction", None)            #动作 
        
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
    def skillId(self):
        return self.__skillId
    
    def set_skillId(self, v):
        self.__skillId = v
        return self
    
    @property
    def skillUser(self):
        return self.__skillUser
    
    def set_skillUser(self, v):
        self.__skillUser = v
        return self
    
    @property
    def equipPosition(self):
        return self.__equipPosition
    
    def set_equipPosition(self, v):
        self.__equipPosition = v
        return self
    
    @property
    def skillType(self):
        return self.__skillType
    
    def set_skillType(self, v):
        self.__skillType = v
        return self
    
    @property
    def defaultSkills(self):
        return self.__defaultSkills
    
    def set_defaultSkills(self, v):
        self.__defaultSkills = v
        return self
    
    @property
    def skillRank(self):
        return self.__skillRank
    
    def set_skillRank(self, v):
        self.__skillRank = v
        return self
    
    @property
    def activeSkills(self):
        return self.__activeSkills
    
    def set_activeSkills(self, v):
        self.__activeSkills = v
        return self
    
    @property
    def skillGoals(self):
        return self.__skillGoals
    
    def set_skillGoals(self, v):
        self.__skillGoals = v
        return self
    
    @property
    def skillName(self):
        return self.__skillName
    
    def set_skillName(self, v):
        self.__skillName = v
        return self
    
    @property
    def breakoutName(self):
        return self.__breakoutName
    
    def set_breakoutName(self, v):
        self.__breakoutName = v
        return self
    
    @property
    def skillDescription(self):
        return self.__skillDescription
    
    def set_skillDescription(self, v):
        self.__skillDescription = v
        return self
    
    @property
    def skillIntroduce(self):
        return self.__skillIntroduce
    
    def set_skillIntroduce(self, v):
        self.__skillIntroduce = v
        return self
    
    @property
    def parm1(self):
        return self.__parm1
    
    def set_parm1(self, v):
        self.__parm1 = v
        return self
    
    @property
    def parm2(self):
        return self.__parm2
    
    def set_parm2(self, v):
        self.__parm2 = v
        return self
    
    @property
    def parm3(self):
        return self.__parm3
    
    def set_parm3(self, v):
        self.__parm3 = v
        return self
    
    @property
    def parm4(self):
        return self.__parm4
    
    def set_parm4(self, v):
        self.__parm4 = v
        return self
    
    @property
    def savedPreset(self):
        return self.__savedPreset
    
    def set_savedPreset(self, v):
        self.__savedPreset = v
        return self
    
    @property
    def skillPreset(self):
        return self.__skillPreset
    
    def set_skillPreset(self, v):
        self.__skillPreset = v
        return self
    
    @property
    def hitPreset(self):
        return self.__hitPreset
    
    def set_hitPreset(self, v):
        self.__hitPreset = v
        return self
    
    @property
    def ballisticsPreset(self):
        return self.__ballisticsPreset
    
    def set_ballisticsPreset(self, v):
        self.__ballisticsPreset = v
        return self     
    
    @property
    def weaponPresets(self):
        return self.__weaponPresets
    
    def set_weaponPresets(self, v):
        self.__weaponPresets = v
        return self
    
    @property
    def spineAction(self):
        return self.__spineAction
    
    def set_spineAction(self, v):
        self.__spineAction = v
        return self
        


