"""
File: bracket.py
Brief: Outlines an individual bracket object. Used in the session object later.
Author: Brandon Dennis
Version: 0.2
Last updated: 8/18/2026
TODO:
Make startRound take a list of integers representing open tables
"""

from Objects.player import *
from Objects.pod import *
from HelperData.exceptions import PlayerNotFound, OverfullGroupError, UnderfullGroupError, PlayerAlreadyGroupedError, PlayerExistsError, UnderfullBracketError
from random import choice, shuffle

class Bracket:
    def __init__(self, name:str, down:bool=False):
        self.name:str = name
        self.isDownstairs:bool = down
        self.__maxSize = 4
        self.__players:list[Player] = []
        self.__groups:list[list[Player]] = []
        self.__pods:list[Pod] = []
        self.__remaining_pods: list[Pod] = []

    @property
    def getPods(self) -> list[Pod]:
        return self.__pods

    @property
    def getPlayers(self) -> list[Player]:
        return self.__players

    @property
    def getGroups(self) -> list[list[Player]]:
        return self.__groups

    # Adds a new player object with a given name to the player list
    def addPlayer(self, name:str) -> Player:
        if self.findPlayer(name):
            raise PlayerExistsError(f"Player with name '{name}' already exists.")
        player = Player(name)
        self.__players.append(player)
        return player

    # Removes a player with a given name from this bracket
    def removePlayer(self, name:str) -> Player:
        for p in self.__players:
            # If the player is found, return them
            if p.name == name:
                # Remove the player from the bracket and any groups they're in
                self.__players.remove(p)
                self.removeGroup(p)
                return p
        # Otherwise, raise an exception
        raise PlayerNotFound(f"Player '{name}' not found in bracket {self.name}.")

    # Searches for a player with a given name and returns it if found
    def findPlayer(self, name:str) -> Player:
        # Search for a player with the given name
        for p in self.__players:
            if p.name == name:
                return p
        # Return none if not found
        return None

    # Creates a group of players from a list of names
    def createGroup(self, members:list[str]):
        # Raise an exception if the group cannot be seated together
        if len(members) > self.__maxSize:
            raise OverfullGroupError(f"Group size {len(members)} exceeds max pod size of {self.__maxSize}.")
        # Raise an exception if the group size is 1. No group needed
        if len(members) == 1:
            raise UnderfullGroupError("Cannot create a group with only one member.")
        group = []
        for m in members:
            # See if each player is already in the bracket
            p = self.findPlayer(m)
            # If not, add them to it
            if p == None:
                p = self.addPlayer(m)
            # Check to see if the player is already in a group.
            else:
                for g in self.__groups:
                    if p in g:
                        raise PlayerAlreadyGroupedError(f"Player {p.name} is already in a group.")
            # Add the finalized list to the groups array
            group.append(p)
            # TESTING: Adding a character to grouped players for testing
            # p.name += " *"
        self.__groups.append(group)

    # Removes a player from a group and removes the group from the bracket list if only one other player is remaining
    def removeGroup(self, player: Player):
        for gr in self.__groups:
            # Remove the specified player
            if player in gr:
                gr.remove(player)
                # After removal, remove the group if only 1 player is left
                if len(gr) == 1:
                    self.__groups.remove(gr)

    # Starts a round by creating pods based on player count and seating all listed players
    def startRound(self, tables:int):
        threeAvg = 0
        downAvg = 0
        # Make sure players are all unseated and collect information on average games played in un-optimal conditions
        for p in self.__players:
            p.unseat()
            threeAvg += p.checkThrees
            downAvg += p.checkDownCount
        # Get an average for games played in 3 pods and downstairs.
        threeAvg = float(threeAvg / len(self.__players))
        downAvg = float(downAvg / len(self.__players))

        # Clear the pods array and re-populate it
        self.__pods = []
        self.__remaining_pods = []
        numPods = self.makePods(tables)

        # Assign groups to tables first
        for g in self.__groups:
            groupPod, threePod, downstairs = self.findPod(g[0], threeAvg, downAvg, len(g))
            for p in g:
                groupPod.addPlayer(p)
                p.seat(threePod, downstairs)
        # Sort all players by the number of non-ideal conditions they've played with so far.
        self.__players = sorted(self.__players, key=lambda p: p.getUnidealCount, reverse=True)
        # Then go through the whole list and seat unseated players
        for p in self.__players:
            if not p.checkSeated:
                soloPod, threePod, downstairs = self.findPod(p, threeAvg, downAvg, 1)
                soloPod.addPlayer(p)
                p.seat(threePod, downstairs)

    # For a particular player, find a suitable pod given their statistics
    def findPod(self, p:Player, threeAvg:int, downAvg:int, groupSize:int) -> tuple[Pod, bool, bool]:
        # Variables needed for re-randomizing
        found = False
        tries = 0
        while not found and tries < 100:
            # Increment a counter to avoid infinite loop
            tries += 1
            # Randomly assign a pod and check its qualities
            pod = choice(self.__remaining_pods)
            threePod = True if pod.getSize == 3 else False
            downstairs = True if "downstairs" in pod.name.lower() else False
            # Check to see if the group can fit in the pod, otherwise re-randomize
            if pod.remaining < groupSize:
                continue
            # If the group is under the average "un-ideal" qualities, assign them to any pod that can fit them
            if p.checkThrees < threeAvg and p.checkDownCount < downAvg:
                found = True
            # Otherwise, check and see if the pod is suitable for the group
            if p.checkThrees > threeAvg and threePod:
                continue
            elif p.checkDownCount > downAvg and downstairs:
                continue
            else:
                found = True
        # If the selected pod is empty after seating, remove it from the available pods.
        if pod.remaining == groupSize:
            self.__remaining_pods.remove(pod)
        return pod, threePod, downstairs

    # Makes a list of pods based on the number of enrolled players
    def makePods(self, tables:int) -> int:
        if len(self.__players) < 3:
            raise UnderfullBracketError(f"Bracket {self.name} doesn't containe enough players to create pods.")
        elif len(self.__players) == 5:
            raise UnderfullBracketError(f"Bracket {self.name} has 5 players. Cannot seat players evenly.")
        # Calculate the number of full pods and 3 pods based on the number of players
        match len(self.__players) % 4:
            # Evenly divisible by 4: All pods are full
            case 0:
                fours = len(self.__players) // 4
                threes = 0
            # Remainder of 1: (players/4) - 2 full pods and 3 3-pods
            case 1:
                fours = len(self.__players) // 4 - 2
                threes = 3
            # Remainder of 2: (players/4) - 1 full pods and 2 3-pods
            case 2:
                fours = len(self.__players) // 4 - 1
                threes = 2
            # Remainder of 3: players/4 full pods and 1 3-pod
            case 3:
                fours = len(self.__players) // 4
                threes = 1
        # Create full pods and find their floor based on remaining tables
        for i in range(fours):
            if i < tables:
                name = f"Table {i + 1}"
            else:
                name = f"Downstairs Table {i - tables + 1}"
            temp_pod = Pod(name)
            self.__pods.append(temp_pod)
            self.__remaining_pods.append(temp_pod)
        # Create 3 pods and find their floor based on remaining tables
        for j in range(threes):
            if j + fours < tables:
                name = f"Table {fours + j + 1}"
            else:
                name = f"Downstairs Table {fours + j - tables + 1}"
            temp_pod = Pod(name, 3)
            self.__pods.append(temp_pod)
            self.__remaining_pods.append(temp_pod)
        shuffle(self.__remaining_pods)
        return fours + threes

    def formatSeating(self) -> str:
        out = f"### Bracket: {self.name}:\n"
        for pod in self.__pods:
            out += str(pod) + '\n'
        return out
