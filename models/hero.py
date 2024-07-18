# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-18
"""

class Hero():
    
    def __init__(self, sn=None, race=None, attributetype=None, quality=None,
                 clazz=None, weapon=None, levMax=None, skid0=None, skid1=None,
                 skid2=None, skid3=None, skid4=None, natures=None, medals=None,
                 rankBase=None, rankMax=None, rankname=None, hpBase=None,
                 atkBase=None,  defBase=None, strengthBase=None, agileBase=None,
                 velocityBase=None, spBase=None, critBase=None, critDmgBase=None,
                 efectBase=None, efectHitBase=None, hitBase=None, dogBase=None,
                 antiBase=None, atkRateBase=None, moveSpdBase=None, hpgrow=None,
                 atkgrow=None, defgrow=None, strengthgrow=None, agilegrow=None,
                 velocitygrow=None, atrange=None, Lines=None, outCastle=None,
                 openingRemarks=None, isRandom=None,isRecruitDrop=None,
                 p_x=None, p_y=None, p_z=None, **kw_args):
        # 基本属性
        self.__sn = sn			                 #id
        self.__race = race	                     #种族
        self.__attributetype = attributetype	 #属性
        self.__quality = quality	 #英雄的稀有度
        self.__clazz = clazz	     #职业 1射手 2战士 3法师 4治疗 5刺客 6辅助 7坦克
        self.__weapon = weapon	     #武器
        self.__levMax = levMax		 #等级上限
        self.__skid0 =  skid0		 #普攻技能ID
        self.__skid1 =  skid1		 #技能1ID
        self.__skid2 =  skid2	     #技能2ID
        self.__skid3 =  skid3		 #技能3ID
        self.__skid4 =  skid4		 #技能4ID
        self.__natures = natures	 #支持的性格
        self.__medals = medals	     #支持的奖章
        self.__rankBase = rankBase   #初始品质
        self.__rankMax = 	rankMax	 #品质上限
        self.__rankname = rankname		 #品质名称
        # 初始数值
        self.__hpBase = 	hpBase		         #生命-初始
        self.__atkBase = 	atkBase		         #攻击-初始
        self.__defBase = 	defBase		         #防御-初始
        self.__strengthBase = strengthBase		 #力量-初始
        self.__agileBase = agileBase	         #敏捷-初始
        self.__velocityBase = velocityBase	     #速度-初始
        self.__spBase = spBase                   #必杀能量值-初始
        self.__critBase = critBase			     #暴击率-初始
        self.__critDmgBase = 	critDmgBase	     #暴击伤害-初始
        self.__efectBase = efectBase	         #效果抵抗-初始
        self.__efectHitBase = efectHitBase       #效果命中-初始
        self.__hitBase = hitBase	             #命中-初始
        self.__dogBase = 	dogBase	             #闪避-初始
        self.__antiBase = antiBase		         #抗暴-初始
        self.__atkRateBase = 	atkRateBase      #攻击间隔-初始
        self.__moveSpdBase = 	moveSpdBase      #移动速度-初始
        # 成长数值
        self.__hpgrow = hpgrow		            #生命成长
        self.__atkgrow = 	atkgrow		        #攻击成长
        self.__defgrow = 	defgrow	            #防御成长
        self.__strengthgrow = strengthgrow      #力量成长
        self.__agilegrow = agilegrow	        #敏捷成长
        self.__velocitygrow = velocitygrow      #速度成长
        self.__atrange = 	atrange             #攻击距离 
        
        # other
        self.__Lines = Lines	                #触发台词
        self.__outCastle = outCastle		    #能否带出关卡
        self.__openingRemarks = openingRemarks	#开场白
        self.__isRandom = isRandom              #0, 不是随机 1, 随机
        self.__isRecruitDrop = isRecruitDrop	#是否抽卡掉落0-不掉落,1-掉落
        self.__new_attrs = kw_args
        
        # position 位置
        self.__p_x = p_x          # x 坐标
        self.__p_y = p_y          # y 坐标
        self.__p_z = p_z          # z 坐标
        
    
    @property
    def sn(self): # 
        return self.__sn
    
    def set_sn(self, sn_new):
        self.__sn = sn_new
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
    def quality(self):
        return self.__quality
    
    def set_quality(self, quality):
        self.__quality = quality
        return self
    
    @property
    def clazz(self):
        return self.__clazz
    
    def set_clazz(self, clazz):
        self.__clazz = clazz
        return self
    
    @property
    def weapon(self):
        return self.__weapon
    
    def set_weapon(self, weapon):
        self.__weapon = weapon
        return self
    
    @property
    def levMax(self):
        return self.__levMax
    
    def set_levMax(self, levMax):
        self.__levMax = levMax
        return self
    
    @property
    def skid0(self):
        return self.__skid0
    
    def set_skid0(self, skid0):
        self.__skid0 = skid0
        return self
    
    @property
    def skid1(self):
        return self.__skid1
    
    def set_skid1(self, skid1):
        self.__skid1 = skid1
        return self
    
    @property
    def skid2(self):
        return self.__skid2
    
    def set_skid2(self, skid2):
        self.__skid2 = skid2
        return self
    
    @property
    def skid3(self):
        return self.__skid3
    
    def set_skid3(self, skid3):
        self.__skid3 = skid3
        return self
    
    @property
    def skid4(self):
        return self.__skid4
    
    def set_skid4(self, skid4):
        self.__skid4 = skid4
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
    def hpBase(self):
        return self.__hpBase
    
    def set_hpBase(self, hpBase):
        self.__hpBase = hpBase
        return self
    
    @property
    def atkBase(self):
        return self.__atkBase
    
    def set_atkBase(self, atkBase):
        self.__atkBase = atkBase
        return self
    
    @property
    def defBase(self):
        return self.__defBase
    
    def set_defBase(self, defBase):
        self.__defBase = defBase
        return self
    
    @property
    def strengthBase(self):
        return self.__strengthBase
    
    def set_strengthBase(self, strengthBase):
        self.__strengthBase = strengthBase
        return self
    
    @property
    def agileBase(self):
        return self.__agileBase
    
    def set_agileBase(self, agileBase):
        self.__agileBase = agileBase
        return self
    
    @property
    def velocityBase(self):
        return self.__velocityBase
    
    def set_velocityBase(self, velocityBase):
        self.__velocityBase = velocityBase
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
    def moveSpdBase(self):
        return self.__moveSpdBase
    
    def set_moveSpdBase(self, moveSpdBase):
        self.__moveSpdBase = moveSpdBase
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
    def strengthgrow(self):
        return self.__strengthgrow
    
    def set_strengthgrow(self, strengthgrow):
        self.__strengthgrow = strengthgrow
        return self
    
    @property
    def agilegrow(self):
        return self.__agilegrow
    
    def set_agilegrow(self, agilegrow):
        self.__agilegrow = agilegrow
        return self
    
    @property
    def velocitygrow(self):
        return self.__velocitygrow
    
    def set_velocitygrow(self, velocitygrow):
        self.__velocitygrow = velocitygrow
        return self
    
    @property
    def atrange(self):
        return self.__atrange
    
    def set_atrange(self, atrange):
        self.__atrange = atrange
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
    def p_x(self):
        return self.__p_x
    
    def set_p_x(self, p_x):
        self.__p_x= p_x
        return self
    
    @property
    def p_y(self):
        return self.__p_y
    
    def set_p_y(self, p_y):
        self.__p_y= p_y
        return self
    
    @property
    def p_z(self):
        return self.__p_z
    
    def set_p_z(self, p_z):
        self.__p_z= p_z
        return self   
    
    @property
    def position(self):
        return self.p_x, self.p_y, self.p_z
    
    def move_position(self,x,y,z):
        return self.set_p_x(x).set_p_y(y).set_p_z(z)
    
    def is_death(self):
        return self.hpBase <= 0 
    
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
    

class HeroHelper():
    """ 交战双方的hero
    heros_a = [Hero(), Hero(), Hero(),]
    heros_b = [Hero(), Hero(), Hero(),]
    A : 
    B : 
    """
    
    def __init__(self, heros_a=[], heros_b=[]):
        self.heros_a = {each.sn:each for each in heros_a}
        self.heros_b = {each.sn:each for each in heros_b}
    
    def get_hero(self, hero_sn):
        if hero_sn in self.heros_a.keys():
            return self.heros_a.get(hero_sn)
        if hero_sn in self.heros_b.keys():
            return self.heros_b.get(hero_sn)
        return None
    