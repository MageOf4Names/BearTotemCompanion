"""
File: player.py
Brief: Outlines the player class utilized in the Bear Totem Companion
Author: Brandon Dennis
Version: 0.2
Last updated: 8/4/2026
TODO:
Add an attribute that contains the names of players in the pod previously
    - Used as exclusion criteria in sorting for the next round
"""

from HelperData.exceptions import SeatingError


"""
This class contains the fields and functionality to describe a player at Bear Totem
Attributes:
name: A public identifier string
__threes: A private value describing the number of 3 pods played in a night
__downCount: A private value describing the number of pods played downstairs
__seated: A private value used to see if a player has already been seated

Functionality:
A player is created using their name as a (semi)-unique identifier.
    Once created, the player can be sat, unsat, and its private values
    can be accessed through getters.
"""
class Player:
    def __init__(self, name:str):
        self.name:str = name
        self.__threes:int = 0
        self.__downCount:int = 0
        self.__seated: bool = False

    @property
    def checkSeated(self) -> bool:
        return self.__seated

    @property
    def checkThrees(self) -> int:
        return self.__threes

    @property
    def checkDownCount(self) -> int:
        return self.__downCount

    @property
    def getUnidealCount(self) -> int:
        return self.__threes + self.__downCount

    # Checks if the player is already seated and, if not, seats them and increments the proper variables
    def seat(self, unfull:bool=False, down:bool=False):
        if self.__seated:
            raise SeatingError(f"Player {self.name} is already seated.")
        self.__seated = True
        if unfull:
            self.__threes += 1
        if down:
            self.__downCount += 1

    # Unseats the player regardless of their seating status
    def unseat(self) -> None:
        self.__seated = False

    def __str__(self):
        return f"Player name: {self.name}\nGames in a 3-pod: {self.__threes}\nGames downstairs: {self.__downCount}\nCurrently seated: {self.__seated}"
