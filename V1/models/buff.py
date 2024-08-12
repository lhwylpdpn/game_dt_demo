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
    
    def reduce_round_action(self):
        if int(self.__buff_round_action) > 0:
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