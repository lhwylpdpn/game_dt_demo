# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-08-01
"""
import json
import copy
from utils.damage import damage
from utils.transposition import trans_postion

class Buff():
    
    def __init__(self, buff_key, buff_value, buff_round_action, buff_back=None):
        self.__buff_key = buff_key
        self.__buff_value = buff_value
        self.__buff_round_action = int(buff_round_action)
        self.__buff_back = buff_back
        # self.__BUFF_HIT_RATE = None                                            # 增加{0}的命中率
        # self.__BUFF_HIT_RATE_BASE = None                                       # 增加{0}%的命中率，并持续{0}行动回合
        # # 攻击失效
        # self.__BUFF_MISS_HIT = None                                            # 攻击失效
        # self.__BUFF_MISS_BASE = None                                           # {0}%机率使攻击无效，并持续{0}行动回合
        # # 攻击范围
        # self.__BUFF_MAX_ATK_DISTANCE = None                                    # 攻击范围增加
        # self.__BUFF_MAX_ATK_DISTANCE_BASE = None                               # 攻击范围最大值增加{0}格，并持续{0}行动回合
        # # 增加移动力
        # self.__BUFF_ROUND_ACTION = None
        # self.__BUFF_ROUND_ACTION_BASE = None
        # # 增加跳跃力
        # self.__BUFF_JUMP_HEIGHT = None
        # self.__BUFF_JUMP_HEIGHT_BASE = None
        # # 增加物理防御
        # self.__BUFF_DEF = None
        # self.__BUFF_DEF_BASE = None
        # # 增加物理攻击
        # self.__BUFF_ATK = None
        # self.__BUFF_ATK_BASE = None
        # # 增加体力上限
        # self.__BUFF_HP = None
        # self.__BUFF_HP_BASE = None
        # # 增加魔法防御
        # self.__BUFF_MAGICAL_DEF = None
        # self.__BUFF_MAGICAL_DEF_BASE = None
    
    def reduce_round_action(self):
        if self.__buff_round_action > 0:
            self.__buff_round_action = self.__buff_round_action - 1
        return self 
    
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
        self.__buff_round_action = v
        return self

    def is_avaliable(self):
        return self.__buff_round_action > 0 or self.__buff_round_action == -1