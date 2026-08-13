"""
File: session.py
Brief: Class outline for a session object used in the Bear Totem Companion Bot
Author: Brandon Dennis
Version: 0.1.0
Last updated: 8/13/2026
TODO: Update remove and change bracket functions to check for grouped players
"""

from Objects.bracket import Bracket
from HelperData.exceptions import PlayerNotFound

class Session:
    def __init__(self, tables:int, name:str):
        self.name:str = name
        self.__tables:int = tables
        self.__round:int = 0
        self.__brackets:list[Bracket] = []
        self.__brackets.append(Bracket("Play to Win", True))
        self.__brackets.append(Bracket("Super Casual"))
        self.__brackets.append(Bracket("Play for Fun"))

    @property
    def listBrackets(self) -> str:
        out = ""
        count = 1
        for br in self.__brackets:
            out += f"Bracket {count}: {br.name}\n"
            count += 1
        return out

    # Returns the name of a specific bracket.
    def getBracket(self, br:int) -> str:
        return self.__brackets[br].name

    # Sets the number of tables available in the main area.
    def setTableCount(self, num:int):
        self.__tables = num

    # Sets a bracket's downstairs value to a specified boolean.
    def setDownstairs(self, br:int, val:bool):
        self.__brackets[br].isDownstairs = val

    # Adds a player to a given bracket
    def addPlayer(self, br:int, name:str):
        self.__brackets[br].addPlayer(name)

    # Removes a player with a given name from their bracket
    def removePlayer(self, name:str):
        for brk in self.__brackets:
            if brk.findPlayer(name):
                brk.removePlayer(name)
                return
        raise PlayerNotFound(f"Player '{name}' not found in this session.")

    # Creates a group for a specific bracket
    def makeGroup(self, br:int, players:tuple[str]):
        self.__brackets[br].createGroup(players)

    # Changes a player with a given name to a new bracket
    def changeBracket(self, br:int, name:str):
        # Check to see if the player is already in a bracket
        for brk in self.__brackets:
            # If so, remove them from the bracket and any groups they're in
            if brk.findPlayer(name):
                p = brk.removePlayer(name)
                brk.removeGroup(p)
                break
        # Add them to the new bracket
        self.addPlayer(br, name)

    # Adds a new bracket for the session
    def makeBracket(self, name:str, downstairs:bool=False):
        self.__brackets.append(Bracket(name, downstairs))

    # Gives a head count for the selected bracket, or all brackets if none is specified
    def playerCount(self, br=None) -> str:
        # If a specific bracket is listed, make it the only entry in the list
        if br != None:
            brList = [self.__brackets[br]]
        # Otherwise, iterate through all brackets
        else:
            brList = self.__brackets

        # Format a message for the given bracket(s)
        out = ""
        for brk in brList:
            out += f"Player count for bracket {brk.name}: {len(brk.getPlayers)}\n"
        return out

    # Gives a list of players in a specified bracket, or all of them if none is given
    def listPlayers(self, br=None) -> str:
        # If a specific bracket is listed, make it the only entry in the list
        if br != None:
            brList = [self.__brackets[br]]
        # Otherwise, iterate through all brackets
        else:
            brList = self.__brackets

        # Format a message for the given bracket(s)
        out = ""
        for brk in brList:
            out += f"Player in bracket {brk.name}:\n"
            for pl in brk.getPlayers:
                out += f"{pl.name}\n"
        return out

    # Starts a round and returns a list of messages containing seating information
    def startRound(self) -> list[str]:
        # Start by incrementing the round count
        self.__round += 1
        out = [f"# Seating for {self.name} round {self.__round}:"]

        tableCount = self.__tables
        for br in self.__brackets:
            # If the bracket is empty, ignore it.
            if len(br.getPlayers) == 0:
                continue
            # Find the right table count for each group
            if br.isDownstairs:
                br.startRound(0)
            else:
                br.startRound(tableCount)
                used = len(br.getPods)
                tableCount = tableCount - used if used <= tableCount else 0
            out.append(br.formatSeating())
        return out

