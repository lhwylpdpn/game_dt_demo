# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-08-01
"""
from .hero import Hero


class Monster(Hero):
    
    def __init__(self, **kwargs):
        super(Monster, self).__init__(**kwargs)