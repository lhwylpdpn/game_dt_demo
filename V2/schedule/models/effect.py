# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-23
"""

# 效果分类
EFFECT_CATEFORIZE = {
    # 触发的条件
    "CONDITION": ["IS_HIT",          # 当被攻击时触发
                  "IS_DEFAULT_HIT",  # 当被普通攻击时触发
                  "IS_WAIT",         # 当不移动时触发
                  "IS_NEAR_HERO",    # 当有队友时触发	{0|0}范围内存在英雄时触发
                  "IS_SKILL_HIT",    # 当被技能攻击时触发
                  "IS_VICTORY",      # 是否战斗胜利
                  "IS_MOVE",         # 当移动时触发
        ],     
     # 形状 范围
    "RANGE": ["ATK_DISTANCE",         # 攻击范围	将攻击范围扩大{0|0}格
              "HIT_LINE",             # 生效范围(线)	以怪物为原点，据据朝向线性延伸{0|0}
              "HIT_RANGE",            # 生效范围(菱形)	以怪物为原点延伸{0|0}格
              "HIT_SQUARE",           # 生效范围(正方形)	以怪物为原点延伸{0|0}格
              "ATK_DISTANCE_CROSS",   # 攻击范围十字	将攻击范围扩大{0|0}格
        ], 
    # 造成的结果
    "RESULR": ["ATK",                      # 物理伤害	{0}%机率造成{0}%物理伤害
               "REPEL_TARGET",             # 击退目标	将敌人击退{0}格
               "PLOT_DESTROY",             # 伤害地块	造成{0}%伤害，hp小于0后消失
               "PLOT_CHANGE",              # 转换地块	将{0}地块转换为{0}地块
               "ADD_HP",                   # 血量恢复	{0}%机率回复体力上限的{0}%
               "ADD_DEF",                  # 物理防御增加	{0}%机率增加物理防御{0}%
               "ADD_MAGICAL_DEF",          # 魔法防御增加	{0}%机率增加魔法防御{0}%
               "ADD_ATK",                  # 物理攻击增加	{0}%机率增加物理攻击{0}%
               "ADD_ATK_DISTANCE",         # 高度影响攻击范围	高低差每{0}格，最大攻击范围加{0}格
               "MOVE_SELF2TARGET",         # 向目标移动	向攻击目标移动{0}格
               "MOVE_TARGET2SELF",         # 使目标向我移动	使攻击目标让自身移动{0}格
               "DEBUFF_ROUND_ACTION_BACK", # 移动距离降低	{0}%机率造成移动力为{0}，并持续{0}行动回合
               "MISS_DAMAGE",              # 攻击失效	{0}%机率使攻击失效
               "BUFF_ADD_HP",              # 自动回血	{0}%机率回血{0}%，并持续{0}行动回合
               "BUFF_HIT_RATE",            # 命中率增加	增加{0}%的命中率，并持续{0}行动回合
               "BUFF_MAX_ATK_DISTANCE",    # 攻击范围最大值增加	攻击范围最大值增加{0}格，并持续{0}行动回合
               "BUFF_ROUND_ACTION",        # 增加移动力	增加移动力{0}格，并持续{0}行动回合
               "BUFF_JUMP_HEIGHT",         # 增加跳跃力	增加跳跃力{0}格，并持续{0}行动回合
               "ATK_BACK",                 # 反击物理伤害	{0}%机率造成{0}%物理伤害
               "BUFF_DEF",                 # 增加物理防御	增加物理防御{0}%，并持续{0}行动回合
               "BUFF_ATK",                 # 增加物理攻击	增加物理攻击{0}%，并持续{0}行动回合
               "BUFF_HP",                  # 增加体力上限	增加体力上限的{0}%，并持续{0}行动回合
               "BUFF_MAGICAL_DEF",         # 增加魔法防御	增加魔法防御{0}%，并持续{0}行动回合
               "TAG_CRIT",                 # 技能可触发暴击
               "TAG_HIT",                  # 技能必中
               "ADD_BUFF_RANGE",           # 增加BUFF生效范围(菱形)
               "ADD_HP_FORMULA_1",         # 血量恢复	回复体力，{0}%*(魔法攻击)
               "ADD_HP_FORMULA_2",         # 血量恢复	回复体力上限的{0}%，并持续{0}行动回合
               "ADD_UNIT_DISTANCE",        # 增加连携距离	增加连携{0}格
               "ADD_EQUIPMENT",            # 增加可装备类型	增加可装备类型{0}
               "ADD_ROLE_EXP",             # 增加角色经验	经验获取提高{0}%
               "ADD_ROUND_ACTION",         # 增加移动力	增加移动力{0}格
               "ADD_JUMP_HEIGHT",          # 增加跳跃力	增加跳跃力{0}格
               "ADD_VELOCITY",             # 增加速度	增加速度{0}
               "REMOVE_DEBUFF",            # 解除DEBUFF	解除{0}的DEBUFF状态
               "ADD_TEAM_ROLE_EXP",        # 添加全队角色经验	经验获取提高{0}%
               "ADD_TEAM_BASE_EXP",        # 添加全队职业经验	经验获取提高{0}%
               "ATK_FORMULA_1",            # 伤害公式	{0}%物理伤害，{0}%*(物理伤害+敏捷)
               "ATK_FORMULA_2",            # 物理伤害	{0}%物理伤害，{0}%*(魔法攻击)
               "ATK_FORMULA_3",            # 光属性魔法伤害	造成{0}%光属性魔法伤害
               "ATK_FORMULA_4",            # 雷属性魔法伤害	{0}%雷属性伤害，{0}%*(魔法攻击)
               "ATK_FORMULA_5",            # 火属性魔法伤害	{0}%火属性伤害，{0}%*(魔法攻击)
               "ATK_FORMULA_6",            # 冰属性魔法伤害	{0}%冰属性伤害，{0}%*(魔法攻击)
               "ATK_FORMULA_7",            # 按生命百分比造成物量伤害	造成物理伤害{0}%-{0}%
               "ATK_MAGICAL_BACK",         # 反击魔法伤害	{0}%机率造成{0}%魔法伤害，{0}%*(魔法攻击)
               "ADD_HIT_RATE",             # 增加命中率	{0}%机率增加命中率{0}%
               "ADD_MAGICAL",              # 魔法攻击增加	{0}%机率增加魔法防御{0}%
               "ADD_BASE_EXP",             # 增加职业经验	经验获取提高{0}%
               "BUFF_MAGICAL_SHIELD",      # 魔法盾	获取一个体力{0}%的魔法盾
               "DEBUFF_PLOT_FIRE",         # 燃烧	造成伤害{0}%的燃烧伤害，并持续{0}回合
               "ATK_BOMB",                 # 爆炸	造成伤害{0}%的爆炸伤害
               "CREATE_PLOT_SQUARE",       # 生成新附着物 生成范围为{0|0}的{0}地格附着物
               "ATK_FORMULA_10",           # 伤害公式	造成{0}%普攻的火系伤害
               "ATK_FORMULA_11",           # 伤害公式	造成{0}%普攻的水系伤害
               "ATK_FORMULA_12",           # 伤害公式	造成{0}%普攻的物理伤害
        ],     
    # 使用限制
    "LIMITATION": ["USE_COUNT"             # 使用次数	技能可使用{0}次
                   "CHANGE_ATK_DISTANCE",  # 地图高度影响攻击范围	攻击范围限制高度，高低差{0}内生效
                   "GET_MAX_EXP",          # 不可叠加经验	不可叠加经验，同类经验取最大值
                   "OPEN_DISTANCE",        # 开启范围	触发开启的范围为{0|0}     
        ] 
}



class Effect():
    
    def __init__(self, **kwargs):
        self.__id = kwargs.get("id", None)                      # 名称	
        self.__key = kwargs.get("key", "")                      # key
        self.__param = kwargs.get("param", [])
        self.__tag = kwargs.get("tag", "")
        # self.__name = kwargs.get("name", None) 	                  # 名称
        # self.__fanction = kwargs.get("fanction", None)	          # 效果描述 格式为 数值+持续时间 数值在前 持续时间在后
        self.__Priority = kwargs.get("Priority", None)	              # 优先级 数字越大优先级越高
        self.__TriggerTime = kwargs.get("TriggerTime", None)	      # DEMO: 1、立即 2、回合开始 3、回合结束 4、战场结算,  5 死亡时候
        self.__Target = kwargs.get("Target", None)	                  # DEMO: 1.敌方单位 2.自身 3：所有地格 4：友方单位（包括自己） 5：友方目标（不包括自己） 6：敌我单位, 7: 所有hero 8:所有monster 9:地块附着单位（英雄，怪物，地块第四层）
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
    
    def is_condition(self): # 是否是 触发的条件
        return self.key in EFFECT_CATEFORIZE["CONDITION"]
    
    def is_range(self): # 形状 范围
        return self.key in EFFECT_CATEFORIZE["RANGE"]
    
    def is_result(self):# 是否是 结果
        return self.key in EFFECT_CATEFORIZE["RESULR"]
    
    def is_limit(self): # 是否是 使用限制
        return self.key in EFFECT_CATEFORIZE["LIMITATION"] 
        
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
    
    def is_gain_buff(self): # 增益buff
        return self.BuffType == 1
    
    def is_loss_buff(self): # 减益buff
        return self.BuffType == 2
    
    def is_buff(self): # 是不是buff
        return self.BuffType in [1,2]
    
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