# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-18
"""
import json
from utils.damage import damage

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
        self.__sn = kwargs.get("sn", None)                         #sn
        self.__HeroID = kwargs.get("HeroID", None)
        self.__Name = kwargs.get("Name", None)
        self.__max_step = kwargs.get("max_step", None)
        self.__normal_attack_range = kwargs.get("normal_attack_range", None) 
        self.__protagonist = kwargs.get("protagonist", 0)          # 是否是主角
        self.__BaseClassID = kwargs.get("BaseClassID", [])
        self.__race = kwargs.get("race", None)                     #种族
        self.__attributetype = kwargs.get("attributetype", None)   #属性
        self.__Quality = kwargs.get("Quality", None)               #英雄的稀有度
        self.__clazz = kwargs.get("clazz", None)                   #职业 1射手 2战士 3法师 4治疗 5刺客 6辅助 7坦克
        self.__Weapon = kwargs.get("Weapon", None)                 #武器
        self.__WeaponsId = kwargs.get("WeaponsId", None)           #武器ID
        self.__levMax = kwargs.get("levMax", None)                 #等级上限
        self.__AvailableSkills = kwargs.get("AvailableSkills", []) # 可用的技能
        self.__Features = kwargs.get("Features", None)        #
        self.__RoundAction = kwargs.get("RoundAction", None)  # 
        self.__JumpHeight = kwargs.get("JumpHeight", [])   # 跳跃的高度 
        self.__skills =  kwargs.get("skills", [])          # 技能
        self.__natures = kwargs.get("natures", [])         #支持的性格
        self.__medals = kwargs.get("medals", None)         #支持的奖章
        self.__rankBase = kwargs.get("rankBase", None)     #初始品质
        self.__rankMax = kwargs.get("rankMax", None)       #品质上限
        self.__rankname = kwargs.get("rankname", None)     #品质名称
        # 初始数值
        self.__HpBase = kwargs.get("Hp", None)                       #生命-初始
        self.__Hp = kwargs.get("Hp", None)                           #生命
        self.__Atk = kwargs.get("Atk", None)                         #攻击-初始
        self.__Def = kwargs.get("Def", None)                         #防御-初始
        self.__MagicalDef = kwargs.get("MagicalDef", None)           #魔法防御
        self.__Strength = kwargs.get("Strength", None)               #力量-初始
        self.__Agile = kwargs.get("Agile", None)                     #敏捷-初始
        self.__Velocity = kwargs.get("Velocity", None)               #速度-初始   行动力
        self.__spBase = kwargs.get("spBase", None)                   #必杀能量值-初始
        self.__critBase = kwargs.get("critBase", None)               #暴击率-初始
        self.__critDmgBase = kwargs.get("critDmgBase", None)         #暴击伤害-初始
        self.__efectBase = kwargs.get("efectBase", None)             #效果抵抗-初始
        self.__efectHitBase = kwargs.get("efectHitBase", None)       #效果命中-初始
        self.__hitBase = kwargs.get("hitBase", None)                 #命中-初始
        self.__dogBase = kwargs.get("dogBase", None)                 #警戒-初始
        self.__antiBase = kwargs.get("antiBase", None)               #抗暴-初始
        self.__atkRateBase = kwargs.get("atkRateBase", None)         #攻击间隔-初始
        self.__AtkDistance = kwargs.get("AtkDistance", [])           #攻击距离
        self.__moveSpdBase = kwargs.get("moveSpdBase", None)         #移动速度-初始
        self.__moveDistanceHighBase = kwargs.get("moveDistanceHighBase", None) #移动距离-高度
        self.__moveDistanceBase = kwargs.get("moveDistanceBase", None)         #移动距离
        self.__hateBase = kwargs.get("hateBase", {})                           # 仇恨
        self.__luckyBase = kwargs.get("luckyBase", None)                       # 运气
        self.__smartBase = kwargs.get("smartBase", None)                       # 灵巧
        # 成长数值
        self.__hpgrow = kwargs.get("hpgrow", [])                  #生命成长
        self.__atkgrow = kwargs.get("atkgrow", [])                #攻击成长
        self.__defgrow = kwargs.get("defgrow", [])                #防御成长
        self.__StrengthRow = kwargs.get("StrengthRow", [])        #力量成长
        self.__AgileRow = kwargs.get("AgileRow", [])              #敏捷成长
        self.__VelocityGrow = kwargs.get("VelocityGrow", [])      #速度成长
        self.__MagicalDefGrow = kwargs.get("MagicalDefGrow", [])  #魔法防御成长
         
        # other
        self.__Lines = kwargs.get("Lines", None)                    #触发台词
        self.__outCastle = kwargs.get("outCastle", None)            #能否带出关卡
        self.__openingRemarks = kwargs.get("openingRemarks", None)  #开场白
        self.__isRandom = kwargs.get("isRandom", None)              #0, 不是随机 1, 随机
        self.__isRecruitDrop = kwargs.get("isRecruitDrop", None)    #是否抽卡掉落0-不掉落,1-掉落
        self.init_data = kwargs
        
        # position 位置
        self.__position = kwargs.get("position")                    #  坐标
    
    def dict_short(self):
        fields = ["sn", "HeroID", "Name", "protagonist", "Hp", "HpBase", "position", "JumpHeight", "skills", "max_step", "normal_attack_range"]
        return self.dict(fields)
    
    def dict(self, fields=[]):
        if not fields:
            fields = list(self.init_data.keys())
        data = {}
        if "skills" in fields:
            data["skills"] = []
            fields.remove("skills")
            for each in self.skills:
                data["skills"].append(each.dict())
        data.update({field: self.__getattribute__(field) for field in fields})
        return data
             
    @property
    def sn(self): # 
        return self.__sn
    
    def set_sn(self, sn_new):
        self.__sn = sn_new
        return self
    
    @property
    def HeroID(self): # 
        return self.__HeroID
    
    def set_HeroID(self, HeroID):
        self.__HeroID = HeroID
        return self
    
    @property
    def Name(self): # 
        return self.__Name
    
    def set_Name(self, v):
        self.__Name = v
        return self

    @property
    def max_step(self): # 
        return self.__max_step
    
    def set_max_step(self, v):
        self.__max_step = v
        return self

    @property
    def normal_attack_range(self): # 
        return self.__normal_attack_range
    
    def set_normal_attack_range(self, v):
        self.__normal_attack_range = v
        return self

    @property
    def protagonist(self): # 
        return self.__protagonist
    
    def set_protagonist(self, v):
        self.__protagonist = v
        return self
    
    @property
    def BaseClassID(self): # 
        return self.__BaseClassID
    
    def set_BaseClassID(self, v):
        self.__BaseClassID = v
        return self
    
    @property
    def race(self):
        return self.__race
    
    def set_race(self, race_new):
        self.__race = race_new
        return self
    
    @property
    def attributetype(self):
        return self.__attributetype
    
    def set_attributetype(self, attributetype):
        self.__attributetype = attributetype
        return self
    
    @property
    def Quality(self):
        return self.__Quality
    
    def set_Quality(self, Quality):
        self.__Quality = Quality
        return self
    
    @property
    def clazz(self):
        return self.__clazz
    
    def set_clazz(self, clazz):
        self.__clazz = clazz
        return self
    
    @property
    def Weapon(self):
        return self.__Weapon
    
    def set_Weapon(self, Weapon):
        self.__Weapon = Weapon
        return self
    
    @property
    def WeaponsId(self):
        return self.__WeaponsId
    
    def set_WeaponsId(self, WeaponsId):
        self.__WeaponsId = WeaponsId
        return self
    
    @property
    def levMax(self):
        return self.__levMax
    
    def set_levMax(self, levMax):
        self.__levMax = levMax
        return self
    
    @property
    def AvailableSkills(self):
        return self.__AvailableSkills
    
    def set_AvailableSkills(self, AvailableSkills):
        self.__AvailableSkills = AvailableSkills
        return self
    
    @property
    def Features(self):
        return self.__Features
    
    def set_Features(self, Features):
        self.__Features = Features
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
    def natures(self):
        return self.__natures
    
    def set_natures(self, natures):
        self.__natures = natures
        return self
    
    @property
    def medals(self):
        return self.__medals
    
    def set_medals(self, medals):
        self.__medals = medals
        return self
    
    @property
    def rankBase(self):
        return self.__rankBase
    
    def set_rankBase(self, rankBase):
        self.__rankBase = rankBase
        return self
    
    @property
    def rankMax(self):
        return self.__rankMax
    
    def set_rankBase(self, rankMax):
        self.__rankMax = rankMax
        return self
    
    @property
    def rankname(self):
        return self.__rankname
    
    def set_rankname(self, rankname):
        self.__rankname = rankname
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
    def Atk(self):
        return self.__Atk
    
    def set_Atk(self, Atk):
        self.__Atk = Atk
        return self
    
    @property
    def Def(self):
        return self.__Def
    
    def set_Def(self, Def):
        self.__Def = Def
        return self
    
    @property
    def MagicalDef(self):
        return self.__MagicalDef
    
    def set_MagicalDef(self, MagicalDef):
        self.__MagicalDef = MagicalDef
        return self
  
    @property
    def Strength(self):
        return self.__Strength
    
    def set_Strength(self, Strength):
        self.__Strength = Strength
        return self
    
    @property
    def Agile(self):
        return self.__Agile
    
    def set_Agile(self, Agile):
        self.__Agile = Agile
        return self
    
    @property
    def Velocity(self):
        return self.__Velocity
    
    def set_Velocity(self, Velocity):
        self.__Velocity = Velocity
        return self
    
    @property
    def spBase(self):
        return self.__spBase
    
    def set_spBase(self, spBase):
        self.__spBase = spBase
        return self
    
    @property
    def critBase(self):
        return self.__critBase
    
    def set_critBase(self, critBase):
        self.__critBase = critBase
        return self
    
    @property
    def critDmgBase(self):
        return self.__critDmgBase
    
    def set_critDmgBase(self, critDmgBase):
        self.__critDmgBase = critDmgBase
        return self
    
    @property
    def efectBase(self):
        return self.__efectBase
    
    def set_efectBase(self, efectBase):
        self.__efectBase = efectBase
        return self
    
    @property
    def efectHitBase(self):
        return self.__efectHitBase
    
    def set_efectHitBase(self, efectHitBase):
        self.__efectHitBase = efectHitBase
        return self
    
    @property
    def hitBase(self):
        return self.__hitBase
    
    def set_hitBase(self, hitBase):
        self.__hitBase = hitBase
        return self

    @property
    def dogBase(self):
        return self.__dogBase
    
    def set_dogBase(self, dogBase):
        self.__dogBase = dogBase
        return self
    
    @property
    def antiBase(self):
        return self.__antiBase
    
    def set_antiBase(self, antiBase):
        self.__antiBase = antiBase
        return self
    
    @property
    def atkRateBase(self):
        return self.__atkRateBase
    
    def set_atkRateBase(self, atkRateBase):
        self.__atkRateBase = atkRateBase
        return self
    
    @property
    def AtkDistance(self):
        return self.__AtkDistance
    
    def set_AtkDistance(self, AtkDistance):
        self.__AtkDistance = AtkDistance
        return self
    
    @property
    def moveSpdBase(self):
        return self.__moveSpdBase
    
    def set_moveSpdBase(self, moveSpdBase):
        self.__moveSpdBase = moveSpdBase
        return self
    
    @property
    def moveDistanceHighBase(self):
        return self.__moveDistanceHighBase
    
    def set_moveDistanceHighBase(self, moveDistanceHighBase):
        self.__moveDistanceHighBase = moveDistanceHighBase
        return self
    
    @property
    def moveDistanceBase(self):
        return self.__moveDistanceBase
    
    def set_moveDistanceBase(self, moveDistanceBase):
        self.__moveDistanceBase = moveDistanceBase
        return self
    
    @property
    def hateBase(self):
        return self.__hateBase
    
    def set_hateBase(self, hateBase, sn): #对某个敌人的仇恨值
        self.__hateBase[sn] = hateBase
        return self
    
    @property
    def luckyBase(self):
        return self.__luckyBase
    
    def set_luckyBase(self, luckyBase): #对某个敌人的仇恨值
        self.__luckyBase = luckyBase
        return self
    
    @property
    def smartBase(self):
        return self.__smartBase
    
    def set_smartBase(self, smartBase): #对某个敌人的仇恨值
        self.__smartBase = smartBase
        return self

    @property
    def hpgrow(self):
        return self.__hpgrow
    
    def set_hpgrow(self, hpgrow):
        self.__hpgrow = hpgrow
        return self
    
    @property
    def atkgrow(self):
        return self.__atkgrow
    
    def set_atkgrow(self, atkgrow):
        self.__atkgrow = atkgrow
        return self    
    
    @property
    def defgrow(self):
        return self.__defgrow
    
    def set_defgrow(self, defgrow):
        self.__defgrow = defgrow
        return self 
    
    @property
    def StrengthRow(self):
        return self.__StrengthRow
    
    def set_StrengthRow(self, StrengthRow):
        self.__StrengthRow = StrengthRow
        return self
    
    @property
    def AgileRow(self):
        return self.__AgileRow
    
    def set_AgileRow(self, AgileRow):
        self.__AgileRow = AgileRow
        return self
    
    @property
    def VelocityGrow(self):
        return self.__VelocityGrow
    
    def set_VelocityGrow(self, VelocityGrow):
        self.__VelocityGrow = VelocityGrow
        return self
    
    @property
    def MagicalDefGrow(self):
        return self.__MagicalDefGrow
    
    def set_MagicalDefGrow(self, MagicalDefGrow):
        self.__MagicalDefGrow = MagicalDefGrow
        return self
   
    @property
    def Lines(self):
        return self.__Lines
    
    def set_Lines(self, Lines):
        self.__Lines = Lines
        return self    
    
    @property
    def outCastle(self):
        return self.__outCastle
    
    def set_outCastle(self, outCastle):
        self.__outCastle = outCastle
        return self
    
    @property
    def openingRemarks(self):
        return self.__openingRemarks
    
    def set_openingRemarks(self, openingRemarks):
        self.__openingRemarks= openingRemarks
        return self
    
    @property
    def isRandom(self):
        return self.__isRandom
    
    def set_isRandom(self, isRandom):
        self.__isRandom= isRandom
        return self
    
    @property
    def isRecruitDrop(self):
        return self.__isRecruitDrop
    
    def set_isRecruitDrop(self, isRecruitDrop):
        self.__isRecruitDrop= isRecruitDrop
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
    
    def move_position(self,x,y,z):
        return self.set_p_x(x).set_p_y(y).set_p_z(z)
    
    def attack(self): # 攻击
        # TODO
        return self
    
    def move_close_enemy(self):
        # TODO
        return self
    
    def move_far_enemy(self):
        # TODO
        return self
    
    def is_death(self):
        return self.Hp <= 0 
    
    def use_skill0(self):
        # TODO
        return self
    
    def use_skill1(self):
        # TODO
        return self
    
    def use_skill2(self):
        # TODO
        return self
    
    def use_skill3(self):
        # TODO
        return self
    
    def use_skill4(self):
        
        # TODO
        return self
    
    def func_attack(self, enemys=[], skill=None): #技能攻击
        # TODO 调用攻击伤害函数
        # self 自己属性的改表
        # 敌人属性的改变
        # 地块的改变
        if not isinstance(enemys, list):
            enemys = [enemys, ]
        for each in enemys:
            result = damage(attacker=self, defender=each, skill=skill)
            _t_hp = each.Hp - result
            each.set_Hp(_t_hp if _t_hp >= 0 else 0) # 血量
        return self