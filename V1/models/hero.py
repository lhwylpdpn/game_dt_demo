# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-08-01
"""
import json
import copy
from utils.damage import damage
from utils.transposition import trans_postion
from utils.tools import random_choices
from .buff import Buff

class Hero():
    
    def __init__(self, **kwargs):
        # 初始数据留存为后续重新初始化做准备
        # 行动力增加自增的函数
        # 移动 - 连带地块对hero属性营销
        # 攻击地块，敌人 - 连带地块
        #
        # skill攻击 - 地块，敌人
        # buff 

        # 基本属性
        self.__HeroID = kwargs.get("HeroID", None)
        self.__protagonist = kwargs.get("protagonist", 0)          # 是否是主角
        self.__AvailableSkills = kwargs.get("AvailableSkills", []) # 可用的技能     #
        self.__RoundAction = kwargs.get("RoundAction", None)       # 行动步数
        self.__JumpHeight = kwargs.get("JumpHeight", [])           # 跳跃的高度 
        self.__skills =  kwargs.get("skills", [])                  # 技能
        self.__DogBase = kwargs.get("DogBase", None)               # 警戒-初始
        # 初始数值
        self.__HpBase = kwargs.get("Hp", None)                       #生命-初始
        self.__Hp = kwargs.get("Hp", None)                           #生命
        
        self.__AtkBase = kwargs.get("Atk", None)                     #攻击-初始
        self.__Atk = kwargs.get("Atk", None)                         #攻击
        
        self.__DefBase = kwargs.get("Def", None)                     #防御-初始
        self.__Def = kwargs.get("Def", None)                         #防御

        self.__MagicalAtkBase = kwargs.get("MagicalAtk", None)       #魔法攻击-初始
        self.__MagicalAtk = kwargs.get("MagicalAtk", None)           #魔法攻击

        self.__MagicalDefBase = kwargs.get("MagicalDef", None)       #魔法防御-初始
        self.__MagicalDef = kwargs.get("MagicalDef", None)           #魔法防御

        self.__AgileBase = kwargs.get("Agile", None)                 #敏捷-初始
        self.__Agile = kwargs.get("Agile", None)                     #敏捷

        self.__VelocityBase = kwargs.get("Velocity", None)           #速度-初始   行动力
        self.__Velocity = kwargs.get("Velocity", None)               #速度-初始   行动力
        
        self.__LuckBase = kwargs.get("Luck", None)                   #运气-初始
        self.__Luck = kwargs.get("Luck", None)                       #运气

        
        # position 位置
        self.__position = list(trans_postion(*kwargs.get("position")))         #  坐标
        self.__avali_move_p_list = kwargs.get("avali_move_p_list", [])         #  可移动范围
        self.__shoot_p_list = kwargs.get("shoot_p_list", [])                   #  可攻击范围
        self.__atk_effect_p_list = kwargs.get("atk_effect_p_list", [])         #  攻击效果范围

        #### buff
        self.__buff = []                                                       # 带的buff

        self.fields =  ["HeroID", "protagonist", "AvailableSkills", "RoundAction", "JumpHeight", "skills",
            "DogBase",  "Hp", "HpBase", "Atk",  "Def", "MagicalAtk",
            "MagicalDef",  "Agile",  "Velocity", 
            "Luck", "position", 
            "avali_move_p_list", "shoot_p_list", "atk_effect_p_list"
            ]
    
    def get_fields(self):
        return self.fields
    
    def dict_short(self):
        fields = ["HeroID",  "protagonist", "Hp", "HpBase", "position", "JumpHeight", "skills",
                   "RoundAction", "DogBase"]
        return self.dict(fields)
    
    def dict_to_view(self, fields=[]):
        data = self.dict(fields)
        if "position" in data.keys():
            data["position"] = list(trans_postion(*data["position"]))
        return data

    def dict(self, fields=[]):
        if not fields:
            fields = copy.deepcopy(self.fields)
        data = {}
        if "skills" in fields:
            data["skills"] = []
            fields.remove("skills")
            for each in self.__skills:
                data["skills"].append(each.dict())
        data.update({field: self.__getattribute__(field) for field in fields})
        return data         
    
    @property
    def HeroID(self): # 
        return self.__HeroID
    
    def set_HeroID(self, HeroID):
        self.__HeroID = HeroID
        return self

    @property
    def protagonist(self): # 
        return self.__protagonist
    
    def set_protagonist(self, v):
        self.__protagonist = v
        return self
    
    @property
    def AvailableSkills(self):
        return self.__AvailableSkills
    
    def set_AvailableSkills(self, AvailableSkills):
        self.__AvailableSkills = AvailableSkills
        return self
    
    @property
    def RoundAction(self):
        return self.__RoundAction
    
    def set_RoundAction(self, RoundAction):
        self.__RoundAction = RoundAction
        return self
    
    @property
    def JumpHeight(self):
        return self.__JumpHeight
    
    def set_JumpHeight(self, JumpHeight):
        self.__JumpHeight = JumpHeight
        return self
    
    @property
    def skills(self):
        return self.__skills
    
    def set_skills(self, v):
        self.__skills = v
        return self
    
    def skills_add(self, skill):
        self.__skills.append(skill)
        return self
    
    @property
    def HpBase(self): # 最高血量
        return self.__HpBase
    
    @property
    def Hp(self):
        return self.__Hp
    
    def set_Hp(self, Hp):
        self.__Hp = Hp
        return self
    
    @property
    def AtkBase(self):
        return self.__AtkBase

    @property
    def Atk(self):
        return self.__Atk
    
    def set_Atk(self, Atk):
        self.__Atk = Atk
        return self
    
    @property
    def DefBase(self):
        return self.__DefBase

    @property
    def Def(self):
        return self.__Def
    
    def set_Def(self, Def):
        self.__Def = Def
        return self

    @property
    def MagicalAtkBase(self):
        return self.__MagicalAtkBase

    @property
    def MagicalAtk(self):
        return self.__MagicalAtk
    
    def set_MagicalAtk(self, v):
        self.__MagicalAtk = v
        return self
    
    @property
    def MagicalDefBase(self):
        return self.__MagicalDefBase
    
    @property
    def MagicalDef(self):
        return self.__MagicalDef
    
    def set_MagicalDef(self, MagicalDef):
        self.__MagicalDef = MagicalDef
        return self
    
    @property
    def AgileBase(self):
        return self.__AgileBase

    @property
    def Agile(self):
        return self.__Agile
    
    def set_Agile(self, Agile):
        self.__Agile = Agile
        return self
    
    @property
    def VelocityBase(self):
        return self.__VelocityBase

    @property
    def Velocity(self):
        return self.__Velocity
    
    def set_Velocity(self, Velocity):
        self.__Velocity = Velocity
        return self

    @property
    def DogBase(self):
        return self.__DogBase
    
    def set_DogBase(self, DogBase):
        self.__DogBase = DogBase
        return self
    
    @property
    def LuckBase(self):
        return self.__LuckBase

    @property
    def Luck(self):
        return self.__Luck
    
    def set_Luck(self, v): 
        self.__Luck = v
        return self

    @property
    def x(self):
        return self.__position[0]
    
    def set_x(self, p_x):
        self.__position[0]= p_x
        return self
    
    @property
    def y(self):
        return self.__position[1]
    
    def set_y(self, p_y):
        self.__position[1]= p_y
        return self
    
    @property
    def z(self):
        return self.__position[2]
    
    def set_z(self, p_z):
        self.__position[2]= p_z
        return self   
    
    @property
    def position(self):
        return self.__position
    
    @property
    def BUFF_HIT_RATE(self): # 增加{0}的命中率
        value = None
        for each in self.__buff:
            if each.__buff_key == "BUFF_HIT_RATE":
                if value is not None:
                    value += int(each.__buff_value)
                else:
                    value = int(each.__buff_value)
        return value

    @property
    def BUFF_MISS_HIT(self): # {0}%机率使攻击无效，并持续{0}行动回合
        value = None
        for each in self.__buff:
            if each.__buff_key == "BUFF_MISS_HIT":
                if value is not None:
                    value += int(each.__buff_value)
                else:
                    value = int(each.__buff_value)
        return value

    @property
    def BUFF_MAX_ATK_DISTANCE(self): # 攻击范围最大值增加{0}格，并持续{0}行动回合
        value = None
        for each in self.__buff:
            if each.__buff_key == "BUFF_MAX_ATK_DISTANCE":
                if value is not None:
                    value += int(each.__buff_value)
                else:
                    value = int(each.__buff_value)
        return value

    def add_buff(self, buff_key, param): # 增加buff
        self.__buff.append(Buff(buff_key, param[0], param[1]))
        if buff_key == "BUFF_ROUND_ACTION": # # 增加移动力{0}格，并持续{0}行动回合
            self.set_RoundAction(self.RoundAction + int(param[0]))
        if buff_key == "BUFF_JUMP_HEIGHT": # # 增加跳跃力{0}格，并持续{0}行动回合
            self.set_JumpHeight([self.JumpHeight[0] + int(param[0])])
        if buff_key == "BUFF_DEF": # 增加物理防御{0}%，并持续{0}行动回合
            self.set_Def(self.Def * (1 + int(param[0])/100.0))
        if buff_key == "BUFF_ATK": # 增加物理攻击{0}%，并持续{0}行动回合
            self.set_Atk(self.Atk * (1 + int(param[0])/100.0))
        if buff_key == "BUFF_HP": # 增加体力上限{0}%，并持续{0}行动回合
            hp = self.Hp +  self.HpBase * int(param[0])/100.0
            self.set_Hp(self.HpBase if hp >= self.HpBase else hp)
        if buff_key == "BUFF_MAGICAL_DEF": # 增加魔法防御{0}%，并持续{0}行动回合
            self.set_MagicalDef(self.MagicalDef * (1 + int(param[0])/100.0))
        return self
    
    def check_buff(self): # 回合结束后，检查buff的加成
        for each in self.__buff:
            if not each.is_avaliable:
                if buff_key == "BUFF_ROUND_ACTION": # # 增加移动力{0}格，并持续{0}行动回合
                    self.set_RoundAction(self.RoundAction - int(param[0]))
                if buff_key == "BUFF_JUMP_HEIGHT": # # 增加跳跃力{0}格，并持续{0}行动回合
                    self.set_JumpHeight([self.JumpHeight[0] - int(param[0])])
                if buff_key == "BUFF_DEF": # 增加物理防御{0}%，并持续{0}行动回合
                    self.set_Def(self.Def * (1 - int(param[0])/100.0))
                if buff_key == "BUFF_ATK": # 增加物理攻击{0}%，并持续{0}行动回合
                    self.set_Atk(self.Atk * (1 - int(param[0])/100.0))
                if buff_key == "BUFF_HP": # 增加体力上限{0}%，并持续{0}行动回合
                    hp = self.Hp -  self.HpBase * int(param[0])/100.0
                    self.set_Hp(hp if hp >= 1 else 1)
                if buff_key == "BUFF_MAGICAL_DEF": # 增加魔法防御{0}%，并持续{0}行动回合
                    self.set_MagicalDef(self.MagicalDef * (1 - int(param[0])/100.0))
                self.__buff.remove(each)
        return self

    @property
    def avali_move_p_list(self):
        return self.__avali_move_p_list
    
    def set_avali_move_p_list(self, v):
        self.__avali_move_p_list = v
        return self 

    @property
    def shoot_p_list(self):
        return self.__shoot_p_list
    
    def set_shoot_p_list(self, v):
        self.__shoot_p_list = v
        return self 

    @property
    def atk_effect_p_list(self):
        return self.__atk_effect_p_list
    
    def set_atk_effect_p_list(self, v):
        self.__atk_effect_p_list = v
        return self 
    
    def move_position(self,x,y,z):
        return self.set_x(x).set_y(y).set_z(z)

    @property
    def is_death(self):
        return self.Hp <= 0
    
    @property
    def is_alive(self):
        return not self.is_death
    
    def get_Skills(self, active=1): # 获取主动 1 or 被动技能 0
        skill = []
        for _ in self.__skills:
            if int(_.ActiveSkills) == active:
                skill.append(_)
        return skill
    
    def load_skill(self, skill): # 记载技能
        for each in skill.effects:
            if each.key in ['ADD_HP', 'ADD_DEF', 'ADD_MAGICAL_DEF', 'ADD_ATK', 'ADD_ATK_DISTANCE']:
                if random_choices({True:int(each.param[0])/100.0, False:1 - int(each.param[0])/100.0}): # 几率判断
                    if each.key == "ADD_HP": # 血是恢复 {0}%机率回复体力上限的{0}%
                        hp = self.Hp +  self.HpBase * int(each.param[1])/100.0
                        self.set_Hp(self.HpBase if hp >= self.HpBase else hp)
                    elif each.key == "ADD_DEF": # 
                        self.set_Def(self.Def * (1 + int(each.param[1])/100.0))
                    elif each.key == "ADD_MAGICAL_DEF": # 
                        self.set_MagicalDef(self.MagicalDef * (1 + int(each.param[1])/100.0))
                    elif each.key == "ADD_ATK": #
                        self.set_Atk(self.Atk * (1 + int(each.param[1])/100.0))
                    elif each.key == "ADD_ATK_DISTANCE": 
                        print("ADD_ATK_DISTANCE unpack!!")
                    else:
                        pass
            else:
                continue
        return self


    def load_init_unActiveSkill(self): # load  buff
        # 初始的时候，增加非主动，非被动触发的技能, 不是被普通攻击 
        for each_skill in self.get_Skills(active=0):
            if "IS_HIT" not in each_skill.avaliable_effects() and\
               "IS_WAIT" not in each_skill.avaliable_effects() and\
               "IS_DEFAULT_HIT" not in each_skill.avaliable_effects(): 
                    for each in each_skill.effects:
                        self.add_buff(buff_key=each.key, param=each.param)
        return self

    def prepare_attack(self, skill): # 被攻击之前，加载主动技能 (作为 施动者 )
        return self.load_skill(skill)

    def skill_move_to_position(self, point, value):
        print("TODO:技能移动", self.position, "move to ", point, "步数：", value)
        return self
    
    def use_skill(self, enemys=[], skill=None, attack_point=[]): # 使用技能后
        if not skill.use_skill().is_avaliable(): # 使用次数减少
            self.__AvailableSkills.remove(skill.skillId)
        # 判断自己是否向敌人移动 #TODO
        if "MOVE_SELF2TARGET" in skill.avaliable_effects():
            move_value = skill.get_effect_by_key("MOVE_SELF2TARGET")[0] # 移动距离
            self.skill_move_to_position(attack_point, move_value)
        # 判断敌人是否向自己移动 
        if "MOVE_TARGET2SELF" in skill.avaliable_effects():
            move_value = skill.get_effect_by_key("MOVE_TARGET2SELF")[0] # 移动距离
            for each_e in enemys:
                if each_e.position.p_x == attack_point[0] and\
                   each_e.position.p_y == attack_point[1] and\
                   each_e.position.p_y == attack_point[2]:
                   each_e.skill_move_to_position(self.position, move_value)
                   continue
        return self

    def before_be_attacked(self, skill):           # 被攻击之前，加载被动技能(作为被攻击对象)
        for each_skill in self.get_Skills(active=0):
            if "IS_HIT" in each_skill.avaliable_effects() : # 被动触发的技能
                if "IS_DEFAULT_HIT" in each_skill.avaliable_effects(): # 被默认技能攻击
                    if int(skill.defaultSkills) == 1: # 技能是默认技能
                        self.load_skill(each_skill)
                else: # 不是被默认攻击时候出发
                    if int(skill.defaultSkills) == 0: # 技能不是默认技能
                        self.load_skill(each_skill)
        return self
    
    def dont_move(self): # 移动不移动
        for each_skill in self.get_Skills(active=0):
            if "IS_HIT" not in each_skill.avaliable_effects():  # 非被动触发的技能
                if "IS_WAIT" in each_skill.avaliable_effects(): # 不移动
                    self.load_skill(each_skill)
        return self
    
    def reduce_buff_round_action(self): # 每次行动后，减少buff中的round_action
        for each in self.__buff:
            each.reduce_round_action()
        return self

    def func_attack(self, enemys=[], skill=None, attack_point=[]): #技能攻击
        """
            @enemys       被攻击敌人对象列表
            @skill        使用的技能对象
            @attack_point 技能释放点位
        """
        # TODO 调用攻击伤害函数
        # self 自己属性的改表
        # 敌人属性的改变
        # 地块的改变
        result = {}
        # if not isinstance(enemys, list):
        #     enemys = [enemys, ]
        self.check_buff()          # 减少buff
        self.prepare_attack(skill)  # 做攻击之前，加载skill相关
        for each in enemys:
            result = damage(attacker=self, defender=each, skill=skill)
            result[each] = copy.deepcopy(result)
            _t_hp = each.Hp - result.get("damage")
            print("Hp <before>: ", each.Hp)
            print("Hp <damaeg>: ", result)
            each.set_Hp(_t_hp if _t_hp >= 0 else 0) # 血量
            print("Hp <after>: ", each.Hp)
        self.use_skill(enemys=enemys, skill=skill, attack_point=attack_point)
        self.reduce_buff_round_action() # 减少buff的round action
        return result