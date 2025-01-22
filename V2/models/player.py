# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-06

"""

from room import Room

class Player():
    
    def __init__(self, **kwargs):
        self.__playerId = kwargs.get("playerId", None)
        self.__room = None                      # 当前所在的房间
        self.__is_ready = False                 # 是否为游戏准备好
        self.__direction = None                 # LocationLeft, LocationRight
        self.__camp = None                      # p1 or p2 (room 里面的第几个玩家)
    
    @property
    def room(self):
        return self.__room

    def set_room(self, room):
        self.__room = room
        if self.room.left_player is None:
            self.room.left_player = self
            self.set_direction = "LocationLeft"
            self.set_camp("p1")
        else:
            self.room.right_player = self
            self.set_direction = "LocationRight"
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
    

    

    
