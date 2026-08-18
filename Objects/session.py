"""
File: session.py
Brief: Class outline for a session object used in the Bear Totem Companion Bot
Author: Brandon Dennis
Version: 0.2
Last updated: 8/18/2026
TODO:
Remove the necessity of the bracket parameter in group:
    Search each bracket for group members and add new players if all remaining players are in a group
    If players are split among groups, return an error
Restructure StartRound to parse out a list of available tables so table numbers aren't repeated
"""

# Imports from other areas of the project.
from Objects.bracket import Bracket
from Objects.player import Player
from HelperData.exceptions import PlayerNotFound, PlayerExistsError

class Session:
    def __init__(self, tables:int, name:str):
        self.name:str = name
        self.__tables:int = tables
        self.__round:int = 0
        self.__players:set[Player] = set()
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

    # Searches for a player with a given name through the whole session, not just one bracket.
    def findPlayer(self, name:str) -> Player:
        for pl in self.__players:
            if pl.name == name:
                return pl
        return None

    # Adds a player to a given bracket
    def addPlayer(self, br:int, name:str):
        if self.findPlayer(name) != None:
            raise PlayerExistsError(f"There is already a player with name {name} in this session")
        pl = self.__brackets[br].addPlayer(name)
        self.__players.add(pl)

    # Removes a player with a given name from their bracket
    def removePlayer(self, name:str):
        for brk in self.__brackets:
            if brk.findPlayer(name):
                pl = brk.removePlayer(name)
                self.__players.remove(pl)
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
                self.__players.remove(p)
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
        out = f"Total player count: {len(self.__players)}"
        for brk in brList:
            out += f"Player count for bracket **{brk.name}**: **{len(brk.getPlayers)}**\n"
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
            out += f"Players in **{brk.name}:**\n```"
            for pl in brk.getPlayers:
                out += f"- {pl.name}\n"
            if len(brk.getPlayers) == 0: out += "This bracket is empty.\n"
            out += "```\n"
        return out

    # Creates and formats a list of groups in the session
    def listGroups(self, br=None) -> str:
        # If a specific bracket is listed, make it the only entry in the list
        if br != None:
            brList = [self.__brackets[br]]
        # Otherwise, iterate through all brackets
        else:
            brList = self.__brackets

        # Format a message for the given bracket(s)
        out = ""
        for brk in brList:
            out += f"Groups in **{brk.name}:**\n"
            for gr in brk.getGroups:
                out += "```"
                for pl in gr:
                    out += f"- {pl.name}\n"
                out += "```\n"
            if len(brk.getGroups) == 0:
                out += "```This bracket is empty.```\n"
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
