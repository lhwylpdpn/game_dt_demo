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
        self.__Quality = kwargs.get("Quality", 0)          # 是否 boss
        self.fields = copy.deepcopy(super().get_fields())
        self.fields.append("Quality")

    @property
    def Quality(self):
        return self.__Quality

    def dict_short(self):
        data = super().dict_short()
        data["Quality"] = self.Quality
        return data