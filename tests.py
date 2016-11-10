import unittest
import dice

#UNIT TESTS :)
class TestAiMethods(unittest.TestCase):

    def test_rand(self):
        result = dice.rand(100)
        self.assertEqual(len(result), 100, "Incorrect number of returned dices")
        for i in result:
            self.assertTrue(1<=i<=6,"Incorrect dice value")

    def test_poker(self):
        result, val = dice.checkPoker([3,3,3,3,3])
        self.assertTrue(result,"Should be Poker")
        self.assertEqual(val, 3, "Poker should return different value")

    def test_no_poker(self):
        result, val = dice.checkPoker([1, 3, 3, 3, 3])
        self.assertFalse(result, "Should not be Poker")
        self.assertEqual(val, 0, "Poker should return 0 value")

    def test_poker_false(self):
        result, val = dice.checkPoker([1, 3, 3, 3])
        self.assertFalse(result, "Should not be Poker")
        self.assertEqual(val, -1, "Poker should return -1 value")

if __name__ == '__main__':
    unittest.main()