# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-23
"""

EFFECT_DETAIL = {
    "PLOT_DESTROY":   {"type":"hit_plant", "rate": "", }, # 伤害地块 造成们{0}%伤害，hp小于0后消失
    "ATK_DISTANCE":   {},                                 # 攻击范围 将攻击范围扩大{0|0}格
    "PLOT_CHANGE":    {},                                 # 转换地块 将{0}地块转换为{0}地块
    "USE_COUNT":      {},                                 # 使用次数 技能可使用{0}次
    "ATK":            {},                                 # 物理伤害 {0}%机率造成{0}%物理伤害
    "HIT_LINE":       {},                                 # 生效范围(线) 以怪物为原点，据据朝向线性延伸{0|0}
    "REPEL_TARGET":   {},                                 # 击退目标 将敌人击退们{0}格
    "IS_PLOT_HEIGHT": {},                                 # 生效高度范围触发 攻击范围限制高度，高低差{0}内生效
    "ADD_HP":         {}, 
    "ADD_DEF":         {},
    "ADD_MAGICAL_DEF": {},
    "ADD_ATK":         {},
    "IS_HIT":             {},
    "IS_DEFAULT_HIT":     {},
    "IS_WAIT":            {},
    "IS_NEAR_HERO":       {},
    "ATK_FORMULA_1":      {},
    "UPDATE_ATK_DISTANCE":{},
    "HIT_RANGE":          {},
    "MOVE_SELF2TARGET":   {},
    "MOVE_TARGET2SELF":   {},
    "DEBUFF_ROUND_ACTION":{},
    "BUFF_MISS_HIT":      {},
    "BUFF_HIT_RATE":{},
    "BUFF_MAX_ATK_DISTANCE":{},
    "BUFF_ROUND_ACTION":{},
    "BUFF_JUMP_HEIGHT":{},
    "ATK_BACK":{},
    "BUFF_DEF":{},
    "BUFF_ATK":{},
    "BUFE_HP":{},
    "CRIT":{},
}


class SkillEffect():
    
    def __init__(self, **kwargs):
        self.__id = kwargs.get("id", None)                      # 名称	
        self.__key = kwargs.get("key", "")                      # key
        self.__param = kwargs.get("param", [])
        self.__tag = kwargs.get("tag", "")
        # self.__name = kwargs.get("name", None) 	                  # 名称
        # self.__fanction = kwargs.get("fanction", None)	          # 效果描述 格式为 数值+持续时间 数值在前 持续时间在后
        self.__Priority = kwargs.get("Priority", None)	              # 优先级 数字越大优先级越高
        self.__TriggerTime = kwargs.get("TriggerTime", None)	      # DEMO: 1、立即 2、回合结束 3、回合结束 4、战场结算
        self.__Target = kwargs.get("Target", None)	                  # DEMO: 1.敌方单位 2.自身 3：所有地格 4：友方单位（包括自己） 5：友方目标（不包括自己） 6：敌我单位
        # self.__durationType = kwargs.get("durationType", None)	  # 持续时间类型 1.回合 2.步数 3.持续存在 4.立刻消失 5.离开地块 6.遭受一次攻击 7.进行一次攻击 8.遭受一次火属性攻击
        # self.__mark = kwargs.get("mark", None)	                  # 标记  BUFF标记 1为燃烧效果 2为冰冻效果 3为淹死状态 4为冰冻状态
        # self.__hitEffect = kwargs.get("hitEffect", None)	          # 受击效果 1受击 2不受击
        self.__BuffType = kwargs.get("BuffType", 0)	                  # Buff类型  0 非buff  1为增益 2为减益
        # self.__effectIcon = kwargs.get("effectIcon", None)	      # 效果icon
        # self.__buffEffect = kwargs.get("buffEffect", None)	      # BUFF效果  BUFF持续过程中的特效
        # self.__buffTrigger = kwargs.get("buffTrigger", None)        # BUFF触发特效
        # self.__duration = kwargs.get("duration", None)              # 特效持续时间 持续到下次开始为 1
        self.__random = None                                          # 有概率情况下，是否在概率中
        self.fields = ["id", "key", "param", "tag", "Priority", "TriggerTime", "Target"]
    
    def dict(self, fields=[]):
        if not fields:
            fields = self.fields
        return {field:self.__getattribute__(field) for field in fields}

    def is_buff(self):
        return self.__BuffType in [1, 2]

    @property
    def id(self):
        return self.__id    
    
    def set_id(self, value):
        self.__id = value
        return self
    
    @property
    def key(self):
        return self.__key
    
    def set_key(self, value):
        self.__key = value
        return self
    
    @property
    def param(self):
        return self.__param
    
    def set_param(self, value):
        self.__param = value
        return self
    
    @property
    def tag(self):
        return self.__tag
    
    def set_tag(self, value):
        self.__tag = value
        return self

    @property
    def random(self):
        return self.__random
    
    def set_random(self, value):
        self.__random = value
        return self
    
    
    # @property
    # def name(self):
    #     return self.__name
    
    # def set_name(self, value):
    #     self.__name = value
    #     return self
    
    # @property
    # def fanction(self):
    #     return self.__fanction
    
    # def set_fanction(self, v):
    #     self.__fanction = v
    #     return self
    
    @property
    def Priority(self):
        return self.__Priority
    
    @property
    def TriggerTime(self):
        return self.__TriggerTime
    
    def set_TriggerTime(self, v):
        self.__TriggerTime
        return self
    
    @property
    def Target(self):
        return self.__Target
    
    def set_Target(self, v):
        self.__Target = v
        return self
    
    # @property
    # def durationType(self):
    #     return self.__durationType
    
    # def set_durationType(self, v):
    #     self.__durationType = v
    #     return self
    
    # @property
    # def mark(self):
    #     return self.__mark
    
    # def set_mark(self, v):
    #     self.__mark = v
    #     return self
    
    # @property
    # def hitEffect(self):
    #     return self.__hitEffect
    
    # def set_hitEffect(self, v):
    #     self.__hitEffect = v
    #     return self
    
    @property
    def BuffType(self):
        return self.__BuffType
    
    def set_BuffType(self, v):
        self.__BuffType = v
        return self
    
    # @property
    # def effectIcon(self):
    #     return self.__effectIcon
    
    # def set_effectIcon(self, v):
    #     self.__effectIcon = v
    #     return self
    
    # @property
    # def buffEffect(self):
    #     return self.__buffEffect
    
    # def set_buffEffect(self, v):
    #     self.__buffEffect = v
    #     return self
    
    # @property
    # def buffTrigger(self):
    #     return self.__buffTrigger
    
    # def set_buffTrigger(self, v):
    #     self.__buffTrigger = v
    #     return self
    
    # @property
    # def duration(self):
    #     return self.__duration
    
    # def set_duration(self, v):
    #     self.__duration = v
    #     return self