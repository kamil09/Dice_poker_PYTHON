import unittest

import ai
import dice

#UNIT TESTS :)
class TestDicesMethods(unittest.TestCase):

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

    def test_kareta_true(self):
        result, val = dice.checkKareta([1,2,2,2,2])
        self.assertTrue(result, "Should be Kareta")
        self.assertEqual(val, 2, "Kareta should return different value")

    def test_kareta_false(self):
        result, val = dice.checkKareta([1,2,4,4,4])
        self.assertFalse(result, "Should not be Kareta")
        self.assertEqual(val, 0, "Kareta should return different value")

    def test_Full_true(self):
        result, val = dice.checkFull([2, 2, 4, 4, 4])
        self.assertTrue(result, "Should be Full")
        self.assertEqual(val, 42, "Full should return different value")

    def test_check_Strit_Small(self):
        result, val = dice.checkStrit([1, 2, 3, 4, 5])
        self.assertTrue(result, "Should be Strit")
        self.assertEqual(val, 1, "Strit should return different value")

    def test_check_Strit_Big(self):
        result, val = dice.checkStrit([2, 3, 4, 5, 6])
        self.assertTrue(result, "Should be Strit")
        self.assertEqual(val, 2, "Strit should return different value")

    def test_check_Strit_false(self):
        result, val = dice.checkStrit([1, 3, 4, 5, 6])
        self.assertFalse(result, "Should not be Strit")
        self.assertEqual(val, 0, "Strit should return different value")

    def test_check_Three_false(self):
        result, val = dice.checkThree([1, 3, 2, 4, 4])
        self.assertFalse(result, "Should not be Three")
        self.assertEqual(val, 0, "Three should return different value")

    def test_check_Three_true(self):
        result, val = dice.checkThree([1, 3, 4, 4, 4])
        self.assertTrue(result, "Should be Three")
        self.assertEqual(val, 4, "Three should return different value")

    def test_check_2pairs_true(self):
        result, val = dice.check2pair([1, 3, 3, 4, 4])
        self.assertTrue(result, "Should be 2 Pairs")
        self.assertEqual(val, 43, "2 Pairs should return different value")

    def test_check_2pairs_false(self):
        result, val = dice.check2pair([1, 2, 3, 4, 4])
        self.assertFalse(result, "Should not be 2 Pairs")
        self.assertEqual(val, 0, "2 Pairs should return different value")

    def test_check_nothing(self):
        result, val = dice.checkNothing([1, 2, 3, 4, 6])
        self.assertTrue(result, "Should be nothing")
        self.assertEqual(val, 6, "2 Pairs should return different value")

    def test_full_poker_game(self):
        testData = [ # (firstList, secondList, whoShouldWin)
            ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6], 2),  #Lets add some test cases to be sure if it's correct
            ([5, 5, 5, 5, 5], [4, 4, 4, 4, 1], 1),
            ([4, 4, 4, 4, 1], [4, 4, 4, 4, 1], 0),
            ([4, 4, 4, 4, 1], [4, 4, 4, 4, 2], 2),
            ([3, 3, 3, 2, 2], [2, 2, 2, 6, 6], 1)
        ]
        for i in testData:
            self.assertEqual(i[2],dice.checkWinner(i[0],i[1]), i)


class TestAIMethod(unittest.TestCase):
    def test_simple_rethrow(self):
        result, rethrow = ai.simpleRethrow([5,5,5,5,5])
        self.assertEqual(len(result),5, "Incorrect array len after rethrowing")
        self.assertEqual(len(rethrow),0, "Shouldn't rethrow good figure")

        result, rethrow = ai.simpleRethrow([2,3,4,5,6])
        self.assertEqual(len(result),5, "Incorrect array len after rethrowing")
        self.assertEqual(len(rethrow),0, "Shouldn't rethrow good figure")

        result, rethrow = ai.simpleRethrow([4, 4, 4, 4, 1])
        self.assertEqual(len(result), 5, "Incorrect array len after rethrowing")
        self.assertEqual(len(rethrow),1, "Shouldn't rethrow good figure")

if __name__ == '__main__':
    unittest.main()