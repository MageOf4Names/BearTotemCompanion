from unittest import TestCase
from Objects.bracket import *

"""
Due to the complexity of the Bracket class, many of the higher level functions are being tested separately.
This test suite is just to make sure the bare functionalities of the class are working as intended.
Things that are tested outside of unit testing include:
- Creation and seeding of pods at the start of a round
- Ensuring seating is following the rules of 3-pods and downstairs tables
- Making sure groups are sat together
- Ensuring the proper types of pods are being created
"""
class TestBracket(TestCase):
    def test_add_player(self):
        bracket = Bracket("Test")
        bracket.addPlayer("Player 1")
        self.assertEqual(bracket.getPlayers[0].name, "Player 1")

    def test_remove_player(self):
        bracket = Bracket("Test")
        bracket.addPlayer("Player 1")
        bracket.removePlayer("Player 1")
        self.assertEqual(bracket.getPlayers, [])

    def test_remove_player_not_found(self):
        bracket = Bracket("Test")
        self.assertRaises(PlayerNotFound, bracket.removePlayer, "Player 1")

    def test_find_player(self):
        bracket = Bracket("Test")
        bracket.addPlayer("Player 1")
        self.assertIsNotNone(bracket.findPlayer("Player 1"))

    def test_groups(self):
        bracket = Bracket("Test")
        bracket.addPlayer("Player 1")
        bracket.addPlayer("Player 2")
        bracket.createGroup(["Player 1", "Player 2"])
        testGroup = bracket.getGroups
        testGroup = [testGroup[0][0].name, testGroup[0][1].name]
        self.assertEqual(testGroup, ["Player 1", "Player 2"])

    def test_group_make_player(self):
        bracket = Bracket("Test")
        bracket.addPlayer("Player 1")
        bracket.createGroup(["Player 1", "Player 2"])
        self.assertIsNotNone(bracket.findPlayer("Player 2"))

    def test_overfull_group(self):
        bracket = Bracket("Test")
        fullGroup = [f"Player {i}" for i in range(5)]
        self.assertRaises(OverfullGroupError, bracket.createGroup, fullGroup)

    def test_underfull_group(self):
        bracket = Bracket("Test")
        fullGroup = ["Player 1"]
        self.assertRaises(UnderfullGroupError, bracket.createGroup, fullGroup)

    def test_group_thrashing(self):
        bracket = Bracket("Test")
        fullGroup = [f"Player {i}" for i in range(4)]
        bracket.createGroup(["Player 1", "Player 2"])
        self.assertRaises(PlayerAlreadyGroupedError, bracket.createGroup, fullGroup)

    def test_pod_count(self):
        bracket = Bracket("Test")
        for i in range(21):
            bracket.addPlayer(f"Player {i}")
        bracket.makePods(7)
        self.assertEqual(len(bracket.getPods), 6)
