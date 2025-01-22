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
        self.__HPBase = kwargs.get("HP", None)                       # 生命-初始
        self.__HP = kwargs.get("HP", None)                           # 生命
        self.__DEFBase = kwargs.get("DEF", None)                     # 防御-初始
        self.__DEF = kwargs.get("DEF", None)                         # 防御
        self.__MDEFBase = kwargs.get("MDEF", None)                   # 魔法防御-初始
        self.__MDEF = kwargs.get("MDEF", None)                       # 魔法防御
        self.__SPDBase = kwargs.get("SPD", None)                     # 速度-初始   行动力
        self.__SPD = kwargs.get("SPD", None)                         # 速度-初始   行动力
        self.__MOVE = kwargs.get("MOVE", None)       # 行动步数
        self.__JUMP = kwargs.get("JUMP", None)           # 跳跃的高度
        
        # 普攻技能相关
        self.__ATKBase = kwargs.get("ATK", None)                     # 攻击-初始
        self.__ATK = kwargs.get("ATK", None)                         # 攻击
        self.__ATKType = kwargs.get("ATKType", None)                 # 攻击属性 1：物理 2：魔法
        self.__ATKDistance = kwargs.get("ATKDistance", None)         # 攻击距离 
        self.__ATKDistanceType = kwargs.get('ATKDistanceType', None) # 攻击距离类型  1菱形， 2 正方形， 3 线
        # magic 攻击相关
        self.__MATKBase = kwargs.get("MATK", None)                    # 攻击-初始
        self.__MATK = kwargs.get("MATK", None)                         # 攻击
        self.__MATKType = kwargs.get("MATKType", None)                 # 攻击属性 1：物理 2：魔法
        self.__MATKDistance = kwargs.get("MATKDistance", None)         # 攻击距离 
        self.__MATKDistanceType = kwargs.get('MATKDistanceType', None) # 攻击距离类型  1菱形， 2 正方形， 3 线

        self.__position = None                                        #  坐标
        self.__init_position = kwargs.get("init_position")            #  初始化时候的相对位置

        self.__camp = None                                            # 阵营 p1, p2 
        
        # 默认属性
        self.__Block = 2                                              # 地块站立的属性 hero 为2， monster 为 3
        
    
    def dict(self):
        fields =  ["HeroID", "MOVE", "JUMP", "HP", "ATK",  "DEF", "MDEF", "MagicalATK",
                   "MagicalDEF",  "SPD",       "position", "ATKType", "ATKDistance",  "ATKDistanceType", 
                   "MATK", "MATKType", "MATKDistance",  "MATKDistanceType", 
                   "camp"]
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
    def MOVE(self):
        return self.__MOVE
    
    @property
    def JUMP(self):
        return self.__JUMP
    
    @property
    def HP(self):
        return self.__HP
    
    def set_HP(self, v):
        self.__HP = v
        return self
    
    @property
    def HPBase(self):
        return self.__HPBase
    
    @property
    def ATK(self):
        return self.__ATK
    
    def set_ATK(self, v):
        self.__ATK = v
        return self
    
    @property
    def ATKBase(self):
        return self.__ATKBase
    
    @property
    def ATKType(self):
        return self.__ATKType
    
    @property
    def ATKDistance(self):
        return self.__ATKDistance
    
    @property
    def ATKDistanceType(self):
        return self.__ATKDistanceType
    
    @property
    def MATK(self):
        return self.__MATK
    
    def set_MATK(self, v):
        self.__MATK = v
        return self
    
    @property
    def MATKBase(self):
        return self.__MATKBase
    
    @property
    def MATKType(self):
        return self.__MATKType
    
    @property
    def MATKDistance(self):
        return self.__MATKDistance
    
    @property
    def MATKDistanceType(self):
        return self.__MATKDistanceType
    
    @property
    def DEF(self):
        return self.__DEF
    
    def set_DEF(self, v):
        self.__DEF = v
        return self
    
    @property
    def MDEF(self):
        return self.__MDEF
    
    def set_MDEF(self, v):
        self.__MDEF = v
        return self
    
    @property
    def DEFBase(self):
        return self.__DEFBase
    
    @property
    def MDEFBase(self):
        return self.__MDEFBase
    
    @property
    def Block(self):
        return self.__Block
    
    @property
    def SPD(self):
        return self.__SPD
    
    def set_SPD(self, v):
        self.__SPD = v
        return self
    
    @property
    def SPDBase(self):
        return self.__SPDBase
    
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
        return self.__HP > 0

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
        # TODO add another attrs

    def dict(self):
        dict_data = super().dict()            # 基础数据
        # TODO add new attr
        return dict_data
    
    def increase_hp(self, delta_hp): # 增加血量
        latest_hp = self.__HP + delta_hp
        self.__HP = self.HPBase if latest_hp >= self.HPBase else latest_hp
        return self
    
    def decrease_hp(self, delta_hp): # 减少血量
        latest_hp = self.__hp - delta_hp
        self.__HP = 0 if latest_hp <= 0 else latest_hp
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
        self.decrease_hp()