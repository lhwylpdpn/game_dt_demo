# -*- coding:utf-8 -*-
"""
author : HU
date: 2025-01-23

"""

class PlayerManagerService():
    
    def __init__(self):
        self.players = {}
    
    def addPlayer(self, player):
        self.players[player.player_id] = players

    def removePlayer(self, player):
        self.players.pop(player.player_id)
    
    def removePlayerByID(self, playerId):
        self.players.pop(playerId)
    
    def getPlayer(self, playerId):
        return self.players.get(playerId)
    
