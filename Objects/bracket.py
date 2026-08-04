"""
File: bracket.py
Brief: Outlines an individual bracket object. Used in the session object later.
Author: Brandon Dennis
Version: 0.0.0
Last updated: 8/4/2026
TODO: Finish startRound function and comments.
"""

from Objects.player import *
from Objects.pod import *
from HelperData.exceptions import PlayerNotFound, OverfullGroupError
from player import Player

class Bracket:
    def __init__(self, name:str, down:bool=False, max=4):
        self.name = name
        self.isDownstairs = down
        self.__players = []
        self.__groups = []
        self.__pods = []
        self.__maxSize = max

    def addPlayer(self, name:str) -> Player:
        player = Player(name)
        self.__players.append(player)
        return player

    def addPlayer(self, player:Player):
        self.__players.append(player)

    def removePlayer(self, name:str) -> Player:
        for p in self.__players:
            if p.name == name:
                self.__players.remove(p)
                return p
        raise PlayerNotFound(f"Player {name} not found in bracket {self.name}.")

    def findPlayer(self, name:str) -> Player:
        for p in self.__players:
            if p.name == name:
                return True

    def createGroup(self, members:list[str]):
        if len(members) > self.__maxSize:
            raise OverfullGroupError(f"Group size {len(members)} exceeds max pod size of {self.__maxSize}.")
        group = []
        for m in members:
            p = self.findPlayer(m)
            if p == None:
                p = self.addPlayer(m)
            group.append(p)
        self.__groups.append(group)
