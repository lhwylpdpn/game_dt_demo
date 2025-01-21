# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-06

"""

class Player():
    
    def __init__(self, **kwargs):
        self.__playerId = kwargs.get("playerId")
        self.__room = None                      # 当前所在的房间
        self.__is_ready = False                 # 是否为游戏准备好
        self.__direction = "left"               # left or right
