# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-17

"""

import os
import json
import uuid
from maps import Map
from cardeffect import CardEffect
from card import Card


class Room():

    def __init__(self, room_id, map_id):
        self.__left_player = None         #  左侧玩家     
        self.__right_player = None        #  右侧玩家
        self.__room_id = room_id          #  房间ID
        self.__round = 0                  #  当前的回合数
        self.__map_id = map_id            #  地图ID
        self.__left_heros = []            #  左侧的英雄 Heros
        self.__right_heros = []           #  右侧的英雄 Heros
        
        # 配置中的信息
        self.__maps = None                #  配置使用的地图
        self.__cards_pool = {}            #  配置中的卡牌 {ID:card, ...}
        self.__heros_pool = {}            #  配置中的英雄 {ID:hero, ...}
        self.__heros_pvp_locations = {}   #  配置中的英雄的初始位置 {LocationLeft:[], LocationRight:[]}
        self.__effects  = {}              #  配置的效果 {ID:cardeffect, .....}
        
    @staticmethod
    def json_data_loader(file_name):
        with open(os.path.join("../tbconfig/", file_name), 'r') as file:
            json_data = json.load(file)
        return json_data
    
    @staticmethod
    def build_room(room_id=None, map_id=1):
        if not room_id:
            room_id = str(uuid.uuid1())
        __room = Room(room_id, map_id)
        # map 地图
        for _ in Room.json_data_loader("tbmap.json"):
            if _["MapID"] == __room.map_id:
                __room.set_maps(Map.build_map(_.get("Details")))
        # 两侧hero的可出生位置
        for _ in Room.json_data_loader("tbmappvp.json"): # LocationLeft:[], LocationRight:[]
            if _["MapID"] == __room.map_id:
                __room.set_heros_pvp_locations(_)
        # card 相关effect 配置数据
        for _ in Room.json_data_loader("tbcardeffect.json"): 
            __room.add_effect(CardEffect(**_))
        # card 相关effect 配置数据
        for _ in Room.json_data_loader("tbcarddetails.json"): 
            new_card = Card(**_)
            for param in new_card.Param:
                new_card.add_effect(__room.get_effect(param.get("id")))
            __room.add_card(new_card)
        return __room
    
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
    def room_id(self):
        return self.__room_id

    @property
    def round(self):
        return self.__round

    def increase_round(self, _round=1):
        self.__round += _round
        return self

    @property
    def maps(self):
        return self.__maps
    
    def set_maps(self, mp_obj):
        self.__maps = mp_obj
        return self
    
    @property
    def map_id(self):
        return self.__map_id

    @property
    def cards_pool(self):
        return self.__cards_pool

    def get_card(self, card_sn):
        return self.__cards_pool.get(card_sn, None)
    
    def add_card(self, card_obj):
        self.cards_pool[card_obj.CardID] = card_obj
        return self
    
    @property
    def heros_pool(self):
        return self.__heros_pool

    def set_heros_pool(self, nw):
        self.__heros_pool = nw
        return self
    
    @property
    def heros_pvp_locations(self):
        return self.__heros_pvp_locations

    def set_heros_pvp_locations(self, nw):
        self.__heros_pvp_locations = nw
        return self
    
    @property
    def effects(self):
        return self.__effects

    def add_effect(self, nw):
        self.__effects[nw.EffectID] = nw
        return self
    
    def get_effect(self, effect_id):
        return self.effects.get(effect_id)
    

if __name__ == "__main__":
    Room.build_room()