# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-23
"""

class SkillEffect():
    
    def __init__(self, **kwargs):
        self.__id = kwargs.get("id", None)                      # 名称	
        self.__key = kwargs.get("key", "")        # key
        self.__param = kwargs.get("param", [])
        self.__tag = kwargs.get("tag", "")
        self.__name = kwargs.get("name", None) 	                  # 名称
        self.__fanction = kwargs.get("fanction", None)	          # 效果描述 格式为 数值+持续时间 数值在前 持续时间在后
        self.__priority = kwargs.get("priority", None)	          # 优先级 数字越大优先级越高
        self.__triggerTime = kwargs.get("triggerTime", None)	  # DEMO: 1、经过该地块 2、回合结束 3、停留在该地块 4、地块被摧毁 5、立刻触发 6，被攻击N次 
                                      # 7，被攻击 8，走一步 9，使用技能时 对自己生效 10，使用技能时 对敌人生效 11，升级技能时 12.使用投掷技能时
        self.__target = kwargs.get("target", None)	              # DEMO: 1.敌方单位 2.自身 3：所有地格 4：友方单位（包括自己） 5：友方目标（不包括自己） 6：敌我单位 7：进入该地格的目标 8：范围内所有地
        self.__durationType = kwargs.get("durationType", None)	  # 持续时间类型 1.回合 2.步数 3.持续存在 4.立刻消失 5.离开地块 6.遭受一次攻击 7.进行一次攻击 8.遭受一次火属性攻击
        self.__mark = kwargs.get("mark", None)	                  # 标记  BUFF标记 1为燃烧效果 2为冰冻效果 3为淹死状态 4为冰冻状态
        self.__hitEffect = kwargs.get("hitEffect", None)	      # 受击效果 1受击 2不受击
        self.__buffType = kwargs.get("buffType", None)	          # Buff类型 1为增益 2为减益
        self.__effectIcon = kwargs.get("effectIcon", None)	      # 效果icon
        self.__buffEffect = kwargs.get("buffEffect", None)	      # BUFF效果  BUFF持续过程中的特效
        self.__buffTrigger	 = kwargs.get("buffTrigger", None)    # BUFF触发特效
        self.__duration = kwargs.get("duration", None)            # 特效持续时间
        self.init_data = kwargs
    
    def dict(self, fields=[]):
        if not fields:
            fields = self.init_data.keys()
        return {field:self.__getattribute__(field) for field in fields}

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
    def name(self):
        return self.__name
    
    def set_name(self, value):
        self.__name = value
        return self
    
    @property
    def fanction(self):
        return self.__fanction
    
    def set_fanction(self, v):
        self.__fanction = v
        return self
    
    @property
    def priority(self):
        return self.__priority
    
    def set_priority(self, v):
        self.__priority = v
        return self
    
    @property
    def triggerTime(self):
        return self.__triggerTime
    
    def set_triggerTime(self, v):
        self.__triggerTime
        return self
    
    @property
    def target(self):
        return self.__target
    
    def set_target(self, v):
        self.__target = v
        return self
    
    @property
    def durationType(self):
        return self.__durationType
    
    def set_durationType(self, v):
        self.__durationType = v
        return self
    
    @property
    def mark(self):
        return self.__mark
    
    def set_mark(self, v):
        self.__mark = v
        return self
    
    @property
    def hitEffect(self):
        return self.__hitEffect
    
    def set_hitEffect(self, v):
        self.__hitEffect = v
        return self
    
    @property
    def buffType(self):
        return self.__buffType
    
    def set_buffType(self, v):
        self.__buffType = v
        return self
    
    @property
    def effectIcon(self):
        return self.__effectIcon
    
    def set_effectIcon(self, v):
        self.__effectIcon = v
        return self
    
    @property
    def buffEffect(self):
        return self.__buffEffect
    
    def set_buffEffect(self, v):
        self.__buffEffect = v
        return self
    
    @property
    def buffTrigger(self):
        return self.__buffTrigger
    
    def set_buffTrigger(self, v):
        self.__buffTrigger = v
        return self
    
    @property
    def duration(self):
        return self.__duration
    
    def set_duration(self, v):
        self.__duration = v
        return self