"""
File: pod.py
Brief: Class outline for the pod object used in Bear Totem Companion
Author: Brandon Dennis
Version: 0.0.0
Last updated: 8/4/2026
TODO:
"""

from Objects.player import *
from HelperData.exceptions import PodOverflowError


"""
This class contains the information for a pod of Magic The Gathering Commander
Attributes:
name: A public identifier for the pod. Usually a table name
__maxSize: A private value representing the max number of players allowed.
__players: A private list of all players in the pod.

Functionality:
Creates a pod of a given name and size, adds players to the table, and utilize
    utility functions to give limited information about the pod.
"""
class Pod:
    def __init__(self, name:str, size:int=4):
        self.name = name
        self.__maxSize = size
        self.__players = []

    # Adds a player to the pod.
    def addPlayer(self, newPlayer:Player):
        if not self.isFull():
            self.__players.append(newPlayer)
        else:
            raise PodOverflowError("This pod is full.")

    # Condenses the main information of the pod into a short string
    def info(self) -> str:
        return f"Name: {self.name}\nPod size: {self.__maxSize}\nPlayers: {len(self.__players)}"

    def getPlayers(self) -> list[Player]:
        return self.__players

    def isFull(self) -> bool:
        return len(self.__players) >= self.__maxSize

    def __str__(self) -> str:
        out = f"{self.name}:\n```\n"
        for p in self.__players:
            out += f"{p.name}\n"
        out += "```"
        return out
