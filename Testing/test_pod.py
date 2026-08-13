from unittest import TestCase
from Objects.pod import *

class TestPod(TestCase):
    # Test the creation of a pod and formatting of the info function
    def test_create(self):
        test = Pod("pod test", 3)
        self.assertEqual(test.info(), "Name: pod test\nPod size: 3\nPlayers: 0")

    # Test the addition of a player
    def test_add_player(self):
        p1 = Player("Test")
        test = Pod("pod test")
        test.addPlayer(p1)
        self.assertEqual(test.getPlayers, [p1])

    # Test if adding too many players raises an error
    def test_overflow(self):
        p1 = Player("Player One")
        p2 = Player("Player Two")
        test = Pod("pod test", 1)
        test.addPlayer(p1)
        self.assertRaises(PodOverflowError, test.addPlayer, p2)

    # Tests if the string method displays in the correct format
    def test_display(self):
        p1 = Player("Player One")
        p2 = Player("Player Two")
        p3 = Player("Player Three")
        p4 = Player("Player Four")
        test = Pod("Test Table", 4)
        test.addPlayer(p1)
        test.addPlayer(p2)
        test.addPlayer(p3)
        test.addPlayer(p4)
        self.assertEqual(str(test),
        """Test Table:
```
Player One
Player Two
Player Three
Player Four
```""")
