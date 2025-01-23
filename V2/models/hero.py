# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-06

"""


class HeroBase(): # hero 基础数据
    
    def __init__(self, **kwargs):
        # 基本属性
        self.__HeroID = int(kwargs.get("HeroID", None))
        self.__BaseClassID = kwargs.get("BaseClassID", None)         # 职业
        self.__AvaliableCards = kwargs.get("AvaliableCards", None)   # 初始卡牌
        self.__HpBase = kwargs.get("Hp", None)                       # 生命-初始
        self.__Hp = kwargs.get("Hp", None)                           # 生命
        self.__DefBase = kwargs.get("Def", None)                     # 防御-初始
        self.__Def = kwargs.get("Def", None)                         # 防御
        self.__DefMagicBase = kwargs.get("DefMagic", None)                   # 魔法防御-初始
        self.__DefMagic = kwargs.get("DefMagic", None)                       # 魔法防御
        self.__SpeedBase = kwargs.get("Speed", None)                     # 速度-初始   行动力
        self.__Speed = kwargs.get("Speed", None)                         # 速度-初始   行动力
        self.__MoveDistance = kwargs.get("MoveDistance", None)       # 行动步数
        self.__JumpHeight = kwargs.get("JumpHeight", None)           # 跳跃的高度
        
        # 普攻技能相关
        self.__AtkBase = kwargs.get("Atk", None)                     # 攻击-初始
        self.__Atk = kwargs.get("Atk", None)                         # 攻击
        self.__AtkType = kwargs.get("AtkType", None)                 # 攻击属性 1：物理 2：魔法
        self.__AtkDistance = kwargs.get("AtkDistance", None)         # 攻击距离 
        self.__AtkDistanceType = kwargs.get('AtkDistanceType', None) # 攻击距离类型  1菱形， 2 正方形， 3 线

        self.__position = None                                        #  坐标
        self.__init_position = kwargs.get("init_position")            #  初始化时候的相对位置

        self.__camp = None                                            # 阵营 p1, p2 
        
        # 默认属性
        self.__Block = 2                                              # 地块站立的属性 hero 为2， monster 为 3
        
    
    def dict(self):
        # fields =  ["HeroID", "MoveDistance", "JumpHeight", "Hp", "Atk",  "Def", "DefMagic", "MagicalAtk",
        #            "MagicalDef",  "Speed",       "position", "AtkType", "AtkDistance",  "AtkDistanceType", 
        #            "camp"]
        fields = [_.replace("__", "") for _ in  self.__dict__.keys()]
        return {_:self.__getattribute__(_) for _ in fields}

    def hero_or_monster(self):
        "HERO or MONSER"
        return self.__class__.__name__.upper()
    
    def is_hero(self):
        return True

    @property    
    def HeroID(self):
        return self.__HeroID
    
    @property
    def BaseClassID(self):
        return self.__BaseClassID
    
    @property
    def MoveDistance(self):
        return self.__MoveDistance
    
    @property
    def JumpHeight(self):
        return self.__JumpHeight
    
    @property
    def Hp(self):
        return self.__Hp
    
    def set_Hp(self, v):
        self.__Hp = v
        return self
    
    @property
    def HpBase(self):
        return self.__HpBase
    
    @property
    def Atk(self):
        return self.__Atk
    
    def set_Atk(self, v):
        self.__Atk = v
        return self
    
    @property
    def AtkBase(self):
        return self.__AtkBase
    
    @property
    def AtkType(self):
        return self.__AtkType
    
    @property
    def AtkDistance(self):
        return self.__AtkDistance
    
    @property
    def AtkDistanceType(self):
        return self.__AtkDistanceType
    
    @property
    def Def(self):
        return self.__Def
    
    def set_Def(self, v):
        self.__Def = v
        return self
    
    @property
    def DefMagic(self):
        return self.__DefMagic
    
    def set_DefMagic(self, v):
        self.__DefMagic = v
        return self
    
    @property
    def DefBase(self):
        return self.__DefBase
    
    @property
    def DefMagicBase(self):
        return self.__DefMagicBase
    
    @property
    def Block(self):
        return self.__Block
    
    @property
    def Speed(self):
        return self.__Speed
    
    def set_Speed(self, v):
        self.__Speed = v
        return self
    
    @property
    def SpeedBase(self):
        return self.__SpeedBase
    
    @property
    def position(self):
        return self.__position
    
    @property
    def camp(self):
        return self.__camp
    
    def set_camp(self, nc):
        self.__camp = nc
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
    
    def set_position(self, v):
        self.__position = v
        return self
    
    @property
    def init_position(self):
        return self.__init_position

    def is_death(self):         # 是不是死亡了
        return self.__Hp > 0

    def is_alive(self):         # 是不是还活着
        return not self.is_death()
   
    ##  被攻击逻辑定义
    def before_hit(self, **kwargs):     # 攻击之前
        pass

    def on_hit(self, **kwargs):         # 命中时
        pass

    def before_hurt(self, **kwargs):    # 被攻击之前
        pass
    
    def on_hurt(self, **kwargs):        # 被攻击
        pass

    def before_killed(self, **kwargs):  # 临终前
        pass
    
    def on_killed(self, **kwargs):      # 被kill时候
        pass
    
    def be_killed(self, **kwargs):      # 被kill之后
        pass
    
    def after_hit(self, **kwargs):      # 攻击之后
        pass
    
    def be_attacked(self, **kwargs):
        self.before_hit(kwargs)
        self.on_hit(kwargs)
        self.before_hurt(kwargs)
        self.on_hurt(kwargs)
        if self.is_death():
            self.before_killed(kwargs)
            self.on_killed(kwargs)
            self.be_killed(kwargs)
        self.after_hit(kwargs)
        return
    
    ## 被救治逻辑定义
    def before_medical(self, **kwargs): # 治疗之前
        pass

    def on_medical_hit(self, **kwargs):  # 治疗命中时候
        pass

    def be_medical(self, **kwargs):      # 被救治 
        pass
    
    def after_medical(self, **kwargs):   # 治疗之后
        pass

    def medical(self, **kwargs):
        self.before_medical(kwargs)
        self.on_medical_hit(kwargs)
        self.be_medical(kwargs)
        self.after_medical(kwargs)
        return


class Hero(HeroBase): # 逻辑相关处理
    
    def __init__(self, **kwargs):
        super(Hero, self).__init__(**kwargs)
        self.__unique_id = None
        # TODO add another attrs

    def dict(self):
        dict_data = super().dict()            # 基础数据
        # TODO add new attr
        return dict_data
    
    def increase_Hp(self, delta_hp): # 增加血量
        latest_hp = self.__Hp + delta_hp
        self.__Hp = self.HpBase if latest_hp >= self.HpBase else latest_hp
        return self
    
    def decrease_Hp(self, delta_hp): # 减少血量
        latest_hp = self.__Hp - delta_hp
        self.__Hp = 0 if latest_hp <= 0 else latest_hp
        return self
    
    def onfocus(self, **kwargs): # 被选中
        pass
    
    def unfocus(self, **kwargs):  # 取消选中
        pass
    
    def move(self, position): # 移动
        self.set_position(position)
        return self
    
    def leve_game(self, state): # 退出战局
        pass
    
    def be_hurt(self):
        self.decrease_Hp()