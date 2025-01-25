# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-17
"""

class EffectBase():
    
    def __init__(self, **kwargs):
        self.__EffectID = kwargs.get("EffectID", None)                # 效果ID	
        self.__Priority = kwargs.get("Priority", None)	              # 优先级 数字越大优先级越高
        self.__TriggerTime = kwargs.get("TriggerTime", None)	      # DEMO: 1、立即触发 2、攻击时候触发 3、手机时候触发 4、回合开始触发,  5 回合结束触发
        self.__Target = kwargs.get("Target", None)	                  # DEMO: 1.地格  2.敌方 3：自身 4：友方
        self.__BuffType = kwargs.get("BuffType", 0)	                  # Buff类型  0 非buff  1为增益 2为减益
        self.__BuffDuration = kwargs.get("BuffDuration", 0)	          # 持续时间类型 1.N回合 2.N韧性 3.受到N次攻击 4.进行N次攻击
        self.__BuffDurationVal = kwargs.get("BuffDurationVal", None)  # 持续时间参数
    
    def dict(self, fields=[]):
        fields = ["EffectID", "Priority", "TriggerTime", "Target", 
                  "BuffType", "BuffDuration", "BuffDurationVal"]
        # fields = [_.replace("__", "") for _ in  self.__dict__.keys()]
        return {field:self.__getattribute__(field) for field in fields}

    # attrs
    @property
    def EffectID(self):
        return self.__EffectID
    
    @property
    def Priority(self):
        return self.__Priority
    
    @property
    def TriggerTime(self):
        return self.__TriggerTime
    
    @property
    def Target(self):
        return self.__Target
    
    @property
    def BuffType(self):
        return self.__BuffType
    
    @property
    def BuffDuration(self):
        return self.__BuffDuration
    
    @property
    def BuffDurationVal(self):
        return self.__BuffDurationVal


class CardEffect(EffectBase):
    
    def __init__(self, **kwargs):
        super(CardEffect, self).__init__(**kwargs)
        
    ## func    
    def is_buff(self):
        return self.BuffType in [1, 2]
    
    def is_gain_buff(self): # 增益buff
        return self.BuffType == 1
    
    def is_loss_buff(self): # 减益buff
        return self.BuffType == 2