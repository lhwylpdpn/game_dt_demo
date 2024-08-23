# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-08-01
"""
import json
import copy
from utils.damage import damage


class Buff():
    
    def __init__(self, buff_key, buff_value, buff_round_action, buff_back=None):
        self.__buff_key = buff_key
        self.__buff_value = buff_value
        self.__buff_round_action = int(buff_round_action)
        self.__buff_back = buff_back
    
    def reduce_round_action(self):
        if self.__buff_round_action > 0:
            self.__buff_round_action = self.__buff_round_action - 1
        return self 
    
    @staticmethod
    def create_buff(hero_or_monster, buff_key, param):
        buff = None
        if buff_key == "DEBUFF_ROUND_ACTION_BACK": # 这个同类别的，后一个覆盖前一个效果
            for each in hero_or_monster.__buff:
                if each.buff_key == "DEBUFF_ROUND_ACTION_BACK":
                    buff = each
                    buff.set_buff_value(param[0]).set_buff_round_action(param[1])
                    continue
            if buff is None: 
                buff = Buff(buff_key, param[0], param[1]).set_buff_back(hero_or_monster.RoundAction)
        else:
            buff = Buff(buff_key, param[0], param[1])
        return buff

    @property
    def buff_back(self):
        return self.__buff_back

    def set_buff_back(self, v):
        self.__buff_back = v
        return self

    @property
    def buff_value(self):
        return self.__buff_value

    def set_buff_value(self, v):
        self.__buff_value = v
        return self
    
    @property
    def buff_key(self):
        return self.__buff_key
    
    @property
    def buff_round_action(self):
        return self.__buff_round_action

    def set_buff_round_action(self, v):
        self.__buff_round_action = int(v)
        return self

    def is_avaliable(self):
        return self.__buff_round_action > 0 or self.__buff_round_action == -1

    def make_invalid(self, hero_or_monster): # 减小buff数值, 使buff失效
        if self.buff_key == "BUFF_ROUND_ACTION": # # 增加移动力{0}格，并持续{0}行动回合
            hero_or_monster.set_RoundAction(hero_or_monster.RoundAction - int(self.buff_value))
        if self.buff_key == "BUFF_JUMP_HEIGHT": # # 增加跳跃力{0}格，并持续{0}行动回合
            hero_or_monster.set_JumpHeight([hero_or_monster.JumpHeight[0] - int(self.buff_value)])
        if self.buff_key == "BUFF_DEF": # 增加物理防御{0}%，并持续{0}行动回合
            hero_or_monster.set_Def(hero_or_monster.Def -  hero_or_monster.DefBase* int(self.buff_value)/100.0)
        if self.buff_key == "BUFF_ATK": # 增加物理攻击{0}%，并持续{0}行动回合
            hero_or_monster.set_Atk(hero_or_monster.Atk -  hero_or_monster.AtkBase *  int(self.buff_value)/100.0)
        if self.buff_key == "BUFF_HP": # 增加体力上限{0}%，并持续{0}行动回合
            hp = hero_or_monster.Hp -  hero_or_monster.HpBase * int(self.buff_value)/100.0
            hero_or_monster.set_Hp(hp if hp >= 1 else 1)
        if hero_or_monster.buff_key == "BUFF_MAGICAL_DEF": # 增加魔法防御{0}%，并持续{0}行动回合
            hero_or_monster.set_MagicalDef(hero_or_monster.MagicalDef - hero_or_monster.MagicalDefBase * int(self.buff_value)/100.0)
        if self.buff_key == "DEBUFF_ROUND_ACTION_BACK": #  around_action {0}，并持续{0}行动回合
            hero_or_monster.set_RoundAction(self.buff_back)
        return hero_or_monster
    
    def make_effective(self, hero_or_monster): # 增加buff数值, 使buff生效
        if self.buff_key == "BUFF_ROUND_ACTION": # # 增加移动力{0}格，并持续{0}行动回合
            hero_or_monster.set_RoundAction(hero_or_monster.RoundAction + int(self.buff_value))
        if self.buff_key == "BUFF_JUMP_HEIGHT": # # 增加跳跃力{0}格，并持续{0}行动回合
            hero_or_monster.set_JumpHeight([hero_or_monster.JumpHeight[0] + int(self.buff_value)])
        if self.buff_key == "BUFF_DEF": # 增加物理防御{0}%，并持续{0}行动回合
            hero_or_monster.set_Def(hero_or_monster.DefBase * (1 + int(self.buff_value)/100.0))
        if self.buff_key == "BUFF_ATK": # 增加物理攻击{0}%，并持续{0}行动回合
            hero_or_monster.set_Atk(hero_or_monster.AtkBase * (1 + int(self.buff_value)/100.0))
        if self.buff_key == "BUFF_HP": # 增加体力上限{0}%，并持续{0}行动回合
            hp = hero_or_monster.Hp +  hero_or_monster.HpBase * int(self.buff_value)/100.0
            hero_or_monster.set_Hp(hero_or_monster.HpBase if hp >= hero_or_monster.HpBase else hp)
        if self.buff_key == "BUFF_MAGICAL_DEF": # 增加魔法防御{0}%，并持续{0}行动回合
            hero_or_monster.set_MagicalDef(hero_or_monster.MagicalDefBase * (1 + int(self.buff_value)/100.0))
        if self.buff_key == "DEBUFF_ROUND_ACTION_BACK": #  around_action {0}，并持续{0}行动回合
            hero_or_monster.set_RoundAction(self.buff_value)
        return hero_or_monster