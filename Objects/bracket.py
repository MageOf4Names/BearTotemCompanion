"""
File: bracket.py
Brief: Outlines an individual bracket object. Used in the session object later.
Author: Brandon Dennis
Version: 0.0.0
Last updated: 8/4/2026
TODO: Optimize findPod to exclude already full pods. Sort players list before seating (otherwise there's a chance it'll fill all the ideal pods first)
"""

from Objects.player import *
from Objects.pod import *
from HelperData.exceptions import PlayerNotFound, OverfullGroupError
from player import Player
from random import randint

class Bracket:
    def __init__(self, name:str, down:bool=False):
        self.name = name
        self.isDownstairs = down
        self.__players = []
        self.__groups = []
        self.__pods = []

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

    def startRound(self, tables:int) -> list[Pod]:
        threeAvg = 0
        downAvg = 0
        # Make sure players are all unseated and collect information on average games played in un-optimal conditions
        for p in self.__players:
            p.unseat()
            threeAvg += p.checkThrees()
            downAvg += p.checkDownCount()
        threeAvg = float(threeAvg / len(self.__players))
        downAvg = float(downAvg / len(self.__players))

        # Clear the pods array and re-populate it
        self.__pods = []
        numPods = self.makePods(tables)

        # Assign groups to tables first
        for g in self.__groups:
            groupPod, threePod, downstairs = self.findPod(g[0], threeAvg, downAvg, len(g))
            for p in g:
                groupPod.addPlayer(p)
                p.seat(threePod, downstairs)
        # Then go through the whole list and seat unseated players
        for p in self.__players:
            if not p.checkSeated():
                soloPod, threePod, downstairs = self.findPod(p)
                soloPod.addPlayer(p)
                p.seat(threePod, downstairs)


    def findPod(self, p:Player, threeAvg:int, downAvg:int, groupSize:int) -> tuple[Pod, bool, bool]:
        found = False
        while not found:
            # Randomly assign a pod and check its qualities
            pod = self.__pods[randint(0, len(self.__pods) - 1)]
            threePod = True if pod.getSize() == 3 else False
            downstairs = True if "downstairs" in pod.name.lower() else False
            # Check to see if the group can fit in the pod, otherwise re-randomize
            if pod.remaining() < groupSize:
                continue
            # If the group is under the average "un-ideal" qualities, assign them to any pod that can fit them
            if p.checkThrees() < threeAvg and p.checkDownCount() < downAvg:
                found = True
            # Otherwise, check and see if the pod is suitable for the group
            if p.checkThrees() > threeAvg and threePod:
                continue
            if p.checkDownCount > downAvg and downstairs:
                continue
        pod.addPlayer(p)
        p.seat(threePod, downstairs)
        return pod, threePod, downstairs

    def makePods(self, tables:int) -> int:
        # Calculate the number of full pods and 3 pods based on the number of players
        match len(self.__players) % 4:
            # Evenly divisible by 4: All pods are full
            case 0:
                fours = len(self.__players) / 4
                threes = 0
            # Remainder of 1: (players/4) - 2 full pods and 3 3-pods
            case 1:
                fours = len(self.__players) / 4 - 2
                threes = 3
            # Remainder of 2: (players/4) - 1 full pods and 2 3-pods
            case 2:
                fours = len(self.__players) / 4 - 1
                threes = 2
            # Remainder of 3: players/4 full pods and 1 3-pod
            case 3:
                fours = len(self.__players) / 4
                threes = 1
        # Create full pods and find their floor based on remaining tables
        for i in range(fours):
            if i < tables:
                name = f"Table {i + 1}"
            else:
                name = f"Downstairs Table {i - tables + 1}"
            self.__pods.append(Pod(name))
        # Create 3 pods and find their floor based on remaining tables
        for j in range(threes):
            if j < tables:
                name = f"Table {i + j + 1}"
            else:
                name = f"Downstairs Table {i + j - tables + 1}"
            self.__pods.append(Pod(name, 3))
        return fours + threes
