# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-06

"""

import copy
from .room import Room
from .device import Device
from .user import User

class Player():
    
    def __init__(self, **kwargs):
        self.__playerId = kwargs.get("playerId", None)
        self.__room = None                      # 当前所在的房间
        self.__is_ready = False                 # 是否为游戏准备好
        self.__direction = None                 # LocationLeft, LocationRight
        self.__camp = None                      # p1 or p2 (room 里面的第几个玩家)
        self.__device = None                    # 设备信息（iphone。 android～～～）
        self.__user = None                      # 玩家信息 （头像，密保，生日，电话, 邮箱～～～）
        self.__ready_game_data = None           # 游戏准备好时候带过来的消息
        self.__show_cards = []                  # 当前round的出牌
    
    def dict(self):
        fields =  ["playerId", "is_ready", "direction", "camp",  "device", "user", "ready_game_data",
                   "show_cards", ]
        data = {_:self.__getattribute__(_) for _ in fields}
        data["room"] = self.room.room_id
        return data
    
    @property
    def ready_game_data(self):
        return self.__ready_game_data

    def set_ready_game_data(self, data):
        self.set_is_ready()
        self.__ready_game_data = data
        self.__init_heros_cards()
        return self
    
    def __init_heros_cards(self):
        for _hero in self.ready_game_data.get("heroes"):
            new_hero = copy.deepcopy(self.room.heros_pool.get(_hero.get("heroId")))
            new_hero.create_unique_id()
            new_hero.set_init_position(_hero.get("position"))
            
            if self == self.room.left_player:
                self.set_direction("LocationLeft")
                self.room.add_left_heros(new_hero)
            if self == self.room.right_player:
                self.set_direction("LocationRight")
                self.room.add_right_heros(new_hero)
            
            new_hero.set_birth_position(self)    # 设置场上的位置
            new_hero.set_camp(self.camp)

            for _card in _hero.get("cardId"):
                new_card = copy.deepcopy(self.room.cards_pool.get(_card))
                new_card.create_unique_id()
                new_hero.add_cards(new_card)

        return self

    @property
    def show_cards(self):
        return self.__show_cards

    @property
    def set_show_cards(self, data):
        self.__show_cards = data
        return self
    
    def use_card(self, unique_id):
        self.__show_cards.remov(unique_id)

    @property
    def room(self):
        return self.__room

    def set_room(self, room):
        self.__room = room
        if self.room.left_player is None:
            self.room.set_left_player(self)
            self.set_direction("LocationLeft")
            self.set_camp("p1")
        else:
            self.room.set_right_player(self)
            self.set_direction("LocationRight")
            self.set_camp("p2")
        return self
    
    def match_player(self, current_avaliable_rooms=[], map_id=1): # 当前服务器的房间状态
        if not current_avaliable_rooms:
            room = Room.build_room()
        else:
            # TODO select room
            room = current_avaliable_rooms[0]
        self.set_room(room)
        return self

    @property
    def playerId(self):
        return self.__playerId

    def set_playerId(self, pid):
        if self.__playerId is None:
            self.__playerId = pid
        return self
    
    @property
    def is_ready(self):
        return self.__is_ready

    def set_is_ready(self):
        self.__is_ready = True
        return self
    
    def unset_is_ready(self):
        self.__is_ready = False
        return self
    
    @property
    def direction(self):
        return self.__direction

    def set_direction(self, dr):
        self.__direction = dr

    @property
    def camp(self):
        return self.__camp

    def set_camp(self, value):
        self.__camp = value
        return self
    
    @property
    def device(self):
        return self.__device

    def set_device(self, value):
        self.__device = value
        return self

    @property
    def user(self):
        return self.__user

    def set_user(self, value):
        self.__user = value
        return self