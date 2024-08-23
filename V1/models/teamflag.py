# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-08-01

"""
import json
import copy
import traceback


class TeamFlag():

    def __init__(self):
        self.__team_id = None
        self.__team_name = None

    @property
    def team_id(self):
        return self.__team_id

    def set_team_id(self, v):
        self.__team_id = v
        return self

    @property
    def team_name(self):
        return self.__team_name

    def set_team_name(self, value):
        self.__team_name = value
        return self
