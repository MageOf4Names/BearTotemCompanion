from unittest import TestCase
from Objects.player import *
from HelperData.exceptions import SeatingError

class TestPlayer(TestCase):
    # Test to see if initilaization and string methods work
    def test_init(self):
        test = Player("Brandon D")
        expected = """Player name: Brandon D
Games in a 3-pod: 0
Games downstairs: 0
Currently seated: False"""
        self.assertEqual(str(test), expected)

    # Check the default seating process
    def test_seat_normal(self):
        test = Player("Test")
        test.seat()
        self.assertTrue(test.checkSeated())

    # Check seating process in a 3-pod
    def test_seat_three(self):
        test = Player("Test")
        test.seat(unfull=True)
        self.assertEqual(test.checkThrees(), 1)

    # Check the seating process for a downstairs game
    def test_seat_down(self):
        test = Player("Test")
        test.seat(down=True)
        self.assertEqual(test.checkDownCount(), 1)

    # Check to see if attempting to seat a seated player results in error
    def test_reseat_error(self):
        test = Player("Test")
        test.seat()
        self.assertRaises(SeatingError, test.seat)

    # Check all functions are working together as intended
    def test_full(self):
        test = Player("Test")
        test.seat(True, False)
        test.unseat()
        test.seat(True, True)
        self.assertEqual(str(test),
        """Player name: Test
Games in a 3-pod: 2
Games downstairs: 1
Currently seated: True""")
