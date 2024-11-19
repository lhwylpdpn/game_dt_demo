# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-08-01
"""
import json
import copy


class Buff():
    
    def __init__(self, buff_id, buff_key, buff_value, buff_round_action, 
                       buff_from=None, buff_back=None, buff_percent=None, 
                       is_need_trigger=False, is_before_action=True, BuffType=None):
        self.__buff_id = buff_id
        self.__buff_key = buff_key
        self.__buff_value = float(buff_value)
        self.__buff_round_action = int(buff_round_action)
        self.__total_buff_round_action = int(buff_round_action)   # 总 round_action
        self.__buff_back = buff_back                 # 用在buff失效后，用来恢复原始值
        self.__buff_from = buff_from                 # buff 是由谁带来的, 默认都是自己的
        self.__buff_percent = buff_percent           # buff 是否触发的百分比（被创建的已经是触发的buff，此数据当前只在返回值用到）
        self.__is_need_trigger =  is_need_trigger    # 是否需要触发执行
        self.__is_before_action = is_before_action   # 是否为行动前需要触发, 默认是 True
        self.__BuffType = BuffType	   # Buff类型  0 非buff  1为增益 2为减益
        self.__fields = ["buff_id", "buff_key", "buff_value", "buff_round_action", 
                         "total_buff_round_action", "buff_back", "is_before_action"]

    def dict(self, **kwargs): # 展示使用
        param =  [self.buff_value, self.buff_round_action]
        if self.__buff_percent:
            param.insert(0, self.__buff_percent)
        return {
            "buff_id": self.buff_id,
            "buff_key": self.buff_key,
            "param":param
        }
    
    def dict_normal(self): 
        return {_:self.__getattribute__(_) for _ in self.__fields} 
    
    def reduce_round_action(self):
        if self.__buff_round_action > 0:
            self.__buff_round_action = self.__buff_round_action - 1
        return self 

    def is_buff(self):
        return self.__BuffType in [1, 2]
    
    @staticmethod
    def create_buff(hero_or_monster, buff_id, buff_key, param, buff_from=None, buff_percent=None, BuffType=None):
        if buff_from is None:
            buff_from = hero_or_monster
        buff = None
        buff_value = param[0]
        buff_round_action = param[1] if len(param) >1 else -1
        if buff_key in ["DEBUFF_ROUND_ACTION_BACK", "DEBUFF_PLOT_FIRE"]: # 这个同类别的，后一个覆盖前一个效果
            for each in hero_or_monster.buff:
                if each.buff_key in ["DEBUFF_ROUND_ACTION_BACK", "DEBUFF_PLOT_FIRE"]:
                    buff = each
                    buff.set_buff_value(buff_value).set_buff_round_action(buff_round_action)
                    continue
            if buff is None: 
                buff = Buff(buff_id, buff_key, buff_value, buff_round_action, 
                            buff_from=buff_from, buff_percent=buff_percent, BuffType=BuffType)
                if buff_key == "DEBUFF_ROUND_ACTION_BACK":
                    buff.set_buff_back(hero_or_monster.RoundAction)
        else:
            buff = Buff(buff_id, buff_key, buff_value, buff_round_action, 
                        buff_from=buff_from, buff_percent=buff_percent, BuffType=BuffType)
            if buff_key in ["BUFF_AD_HP", "BUFF_HP"]:
                buff.set_is_need_trigger(True)
        return buff
    
    @property
    def buff_id(self):
        return self.__buff_id

    @property
    def is_need_trigger(self):
        return self.__is_need_trigger

    def set_is_need_trigger(self, bv):
        self.__is_need_trigger = bv
        return self

    @property
    def buff_back(self):
        return self.__buff_back

    def set_buff_back(self, v):
        self.__buff_back = v
        return self
    
    @property
    def BuffType(self):
        return self.__BuffType
    
    def set_BuffType(self, v):
        self.__BuffType = v
        return self

    @property
    def buff_value(self):
        return float(self.__buff_value)

    def set_buff_value(self, v):
        self.__buff_value = v
        return self
    
    @property
    def buff_key(self):
        return self.__buff_key
    
    @property
    def buff_from(self):
        return self.__buff_from
    
    @property
    def buff_round_action(self):
        return self.__buff_round_action

    def set_buff_round_action(self, v):
        self.__buff_round_action = int(v)
        return self
    
    @property
    def total_buff_round_action(self):
        return self.__total_buff_round_action
    
    @property
    def is_before_action(self):
        return self.__is_before_action
    
    def set_is_before_action(self, v):
        self.__is_before_action = v
        return self

    def is_avaliable(self):
        return self.__buff_round_action > 0 or self.__buff_round_action == -1

    def make_invalid(self, hero_or_monster): # 减小buff数值, 使buff失效
        if self.buff_key == "BUFF_ROUND_ACTION": # # 增加移动力{0}格，并持续{0}行动回合
            hero_or_monster.set_RoundAction(hero_or_monster.RoundAction - self.buff_value)
        elif self.buff_key == "BUFF_UNIT_DISTANCE": # # 增加连携{0}，并持续{0}行动回合
            hero_or_monster.set_UnitDistance(hero_or_monster.UnitDistance - self.buff_value)
        elif self.buff_key == "BUFF_JUMP_HEIGHT": # # 增加跳跃力{0}格，并持续{0}行动回合
            hero_or_monster.set_JumpHeight([hero_or_monster.JumpHeight[0] - self.buff_value])
        elif self.buff_key == "BUFF_DEF": # 增加物理防御{0}%，并持续{0}行动回合
            hero_or_monster.set_Def(hero_or_monster.Def -  hero_or_monster.DefBase * self.buff_value/100.0)
        elif self.buff_key == "BUFF_ATK": # 增加物理攻击{0}%，并持续{0}行动回合
            hero_or_monster.set_Atk(hero_or_monster.Atk -  hero_or_monster.AtkBase *  self.buff_value/100.0)
        # elif self.buff_key == "BUFF_HP": # 增加体力上限{0}%，并持续{0}行动回合
        #     hp = hero_or_monster.Hp -  hero_or_monster.HpBase * int(self.buff_value)/100.0
        #     hero_or_monster.set_Hp(hp if hp >= 1 else 1)
        elif self.buff_key == "BUFF_MAGICAL_DEF": # 增加魔法防御{0}%，并持续{0}行动回合
            hero_or_monster.set_MagicalDef(hero_or_monster.MagicalDef - hero_or_monster.MagicalDefBase * self.buff_value/100.0)
        elif self.buff_key == "DEBUFF_ROUND_ACTION_BACK": #  around_action {0}，并持续{0}行动回合
            hero_or_monster.set_RoundAction(self.buff_back)
        else:
            pass
        return hero_or_monster
    
    def make_effective(self, hero_or_monster): # 增加buff数值, 使buff生效
        effect_attr, delta_change = None, None
        if self.buff_key == "BUFF_ROUND_ACTION": # # 增加移动力{0}格，并持续{0}行动回合
            effect_attr, delta_change = "RoundAction", self.buff_value
            hero_or_monster.set_RoundAction(hero_or_monster.RoundAction + delta_change)
        elif self.buff_key == "BUFF_UNIT_DISTANCE": # # 增加连携{0}，并持续{0}行动回合
            effect_attr, delta_change = "UnitDistance", self.buff_value
            hero_or_monster.set_UnitDistance(hero_or_monster.UnitDistance + delta_change)
        elif self.buff_key == "BUFF_JUMP_HEIGHT": # # 增加跳跃力{0}格，并持续{0}行动回合
            effect_attr, delta_change = "JumpHeight", self.buff_value
            hero_or_monster.set_JumpHeight([hero_or_monster.JumpHeight[0] + delta_change])
        elif self.buff_key == "BUFF_DEF": # 增加物理防御{0}%，并持续{0}行动回合
            effect_attr, delta_change = "Def", hero_or_monster.DefBase * self.buff_value/100.0
            hero_or_monster.set_Def(hero_or_monster.DefBase + delta_change)
        elif self.buff_key == "BUFF_ATK": # 增加物理攻击{0}%，并持续{0}行动回合
            effect_attr, delta_change = "ATK", hero_or_monster.AtkBase * self.buff_value/100.0
            hero_or_monster.set_Atk(hero_or_monster.AtkBase + delta_change)
        elif self.buff_key == "BUFF_ADD_HP": # 自动回血 {0}机率回血{0}，并持续{0}行动回合
            effect_attr, delta_change = "Hp", hero_or_monster.HpBase * self.buff_value/100.0
            hero_or_monster.set_Hp(hero_or_monster.Hp +  delta_change)
        elif self.buff_key == "BUFF_HP": # 增加体力上限{0}%，并持续{0}行动回合
            effect_attr, delta_change = "Hp", hero_or_monster.HpBase * self.buff_value/100.0
            hp = hero_or_monster.Hp +  delta_change
            hero_or_monster.set_Hp(hero_or_monster.HpBase if hp >= hero_or_monster.HpBase else hp)
        elif self.buff_key == "BUFF_MAGICAL_DEF": # 增加魔法防御{0}%，并持续{0}行动回合
            effect_attr, delta_change = "MagicalDef", hero_or_monster.MagicalDefBase * self.buff_value/100.0
            hero_or_monster.set_MagicalDef(hero_or_monster.MagicalDefBase + delta_change)
        elif self.buff_key == "DEBUFF_ROUND_ACTION_BACK": #  around_action {0}，并持续{0}行动回合
            effect_attr, delta_change = "RoundAction", self.buff_value
            hero_or_monster.set_RoundAction(self.buff_value)
        elif self.buff_key == "ADD_HP_FORMULA_2": # 恢复体力上限的{0}%，并持续{0}行动回合
            effect_attr, delta_change = "Hp", hero_or_monster.HpBase * self.buff_value/100.0
            hp = hero_or_monster.Hp +  delta_change
            hero_or_monster.set_Hp(hero_or_monster.HpBase if hp >= hero_or_monster.HpBase else hp)
        elif self.buff_key == "ADD_HP": # 恢复体力上限的{0}%，并持续{0}行动回合
            effect_attr, delta_change = "Hp", hero_or_monster.HpBase * self.buff_value/100.0
            hp = hero_or_monster.Hp +  delta_change
            hero_or_monster.set_Hp(hero_or_monster.HpBase if hp >= hero_or_monster.HpBase else hp)
        elif self.buff_key == "DEBUFF_PLOT_FIRE": #  fire 伤害 {0}，并持续{0}行动回合
            effect_attr, delta_change = "Hp", self.buff_value
            hp = hero_or_monster.Hp - delta_change
            hero_or_monster.set_Hp(hp)
        else:
            pass
        result = [effect_attr, [hero_or_monster.hero_or_monster().lower(),  hero_or_monster.HeroID], delta_change]
        return result