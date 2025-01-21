# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-17

"""

from maps import Map


class Room():

    def __init__(self, game_id, map_id):
        self.__left_player = None         #  左侧玩家     
        self.__right_player = None        #  右侧玩家
        self.__game_id = game_id          #  房间ID
        self.__round = 0                  #  当前的回合数
        self.__maps = None                #  使用的地图
        self.__cards_pool = {}            #  总体的卡牌
        self.__left_heros = []            #  左侧的英雄 Heros
        self.__right_heros = []           #  右侧的英雄 Monster

    def load_map(self, map_id):
        self.__maps = 
    
    @staticmethod
    def create_room(game_id, map_id):
        return Room(game_id, map_id)
    
    @property
    def left_player(self):
        return self.__left_player

    def set_player(self, pl):
        self.__left_player = pl
        return self
    
    @property
    def left_heros(self):
        return self.__left_heros
    
    def add_left_heros(self, nw):
        self.__left_heros.append(nw)
        return self
    
    def remove_from_left_hero(self, dh):
        for _ in self.__left_heros:
            if _.HeroID == dh.__HeroID:
                if _.is_death():
                    self.__left_heros.remove(_)
        return self
    
    def remove_from_right_hero(self, dh):
        for _ in self.__right_heros:
            if _.HeroID == dh.__HeroID:
                if _.is_death():
                    self.__left_heros.remove(_)
        return self

    @property
    def right_heros(self):
        return self.__right_heros
    
    def add_right_heros(self, nw):
        self.__right_heros.append(nw)
        return self

    @property
    def right_player(self):
        return self.__right_player
    
    def set_right_player(self, pl):
        self.__right_player = pl
        return self

    @property
    def right_player(self):
        return self.__right_player
    
    @property
    def game_id(self):
        return self.__game_id

    @property
    def round(self):
        return self.__round

    def increase_round(self, _round=1):
        self.__round += _round
        return self

    @property
    def map(self):
        return self.__map
    
    def set_map(self, mp_obj):
        self.__map = mp_obj
        return self

    @property
    def cards_pool(self):
        return self.__cards_pool

    def get_card(self, card_sn):
        return self.__cards_pool.get(card_sn, None)