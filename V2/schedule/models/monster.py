# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-08-01
"""
import copy
from .hero import Hero


class Monster(Hero):
    
    def __init__(self, **kwargs):
        super(Monster, self).__init__(**kwargs)
        self.__Block = 3                                   # 地块站立的属性 hero 为2， monster 为 3
    
    def is_hero(self):
        return False