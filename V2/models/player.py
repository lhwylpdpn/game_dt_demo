# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-06

"""

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
    
    def dict(self):
        # fields =  ["HeroID", "MoveDistance", "JumpHeight", "Hp", "Atk",  "Def", "DefMagic", "MagicalAtk",
        #            "MagicalDef",  "Speed",       "position", "AtkType", "AtkDistance",  "AtkDistanceType", 
        #            "camp"]
        fields = [_.replace("__", "") for _ in  self.__dict__.keys()]
        return {_:self.__getattribute__(_) for _ in fields}

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
        self.__playerId = pid
    
    @property
    def is_ready(self):
        return self.__is_ready

    def set_is_ready(self, is_ready):
        self.__is_ready = is_ready
    
    @property
    def direction(self):
        return self.__direction

    def set_direction(self, dr):
        self.__direction = dr

    @property
    def camp(self):
        return self.__direction

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
    
