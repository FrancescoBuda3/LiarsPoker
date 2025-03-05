import unittest
from src.model.deck import Card
from src.model.deck.suit import Suit
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.model.stake.impl import StakeHandlerImpl


class TestStakeHandlerImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_STAKE = Stake([2, 5], Combination.TWO_PAIR)
        cls.TEST_CARDS = [Card(2, Suit.HEARTS), Card(2, Suit.DIAMONDS), Card(5, Suit.SPADES), Card(5, Suit.CLUBS)]
        cls.TEST_INVALID_CARDS = [Card(2, Suit.HEARTS), Card(2, Suit.DIAMONDS), Card(5, Suit.SPADES)]

    def setUp(self):
        self.stakeHanlder = StakeHandlerImpl()
        
    def test_get_stake(self):
        self.stakeHanlder.set_stake(self.TEST_STAKE)
        self.assertEqual(self.stakeHanlder.get_stake(), self.TEST_STAKE)
        
    def test_stake_not_set(self):
        with self.assertRaises(ValueError):
            self.stakeHanlder.get_stake()
            
    def test_check_cards(self):
        self.stakeHanlder.set_stake(self.TEST_STAKE)
        self.assertTrue(self.stakeHanlder.check_cards(self.TEST_CARDS))
        
    def test_check_invalid_cards(self):
        self.stakeHanlder.set_stake(self.TEST_STAKE)
        self.assertFalse(self.stakeHanlder.check_cards(self.TEST_INVALID_CARDS))


if __name__ == "__main__":
    unittest.main()
