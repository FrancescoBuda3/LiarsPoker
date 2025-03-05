import unittest
from src.model.deck import Card
from src.model.deck.suit import Suit
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.model.stake.impl import StakeHandlerImpl


class TestStakeHandlerImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_STAKE = Stake([], Combination.HIGH_CARD)
        cls.TEST_TWO_PAIR = Stake([2, 5], Combination.TWO_PAIR)
        cls.TEST_TWO_PAIR_CARDS = [Card(Suit.SPADES, 2), Card(Suit.HEARTS, 2), Card(Suit.SPADES, 5), Card(Suit.HEARTS, 5)]
        cls.TEST_INVALID_TWO_PAIR_CARDS = [Card(Suit.SPADES, 2), Card(Suit.HEARTS, 5), Card(Suit.SPADES, 5)]
        cls.TEST_ROYAL_FLUSH = Stake([], Combination.ROYAL_FLUSH)
        cls.TEST_ROYAL_FLUSH_CARDS = [Card(Suit.SPADES, 10), Card(Suit.SPADES, 11), Card(Suit.SPADES, 12), Card(Suit.SPADES, 13), Card(Suit.SPADES, 14)]
        cls.TEST_INVALID_ROYAL_FLUSH_CARDS = [Card(Suit.SPADES, 10), Card(Suit.SPADES, 11), Card(Suit.SPADES, 12), Card(Suit.SPADES, 13), Card(Suit.SPADES, 2)]

    def setUp(self):
        self.stakeHanlder = StakeHandlerImpl()
        
    def test_get_stake(self):
        self.stakeHanlder.set_stake(self.TEST_STAKE)
        self.assertEqual(self.stakeHanlder.get_stake(), self.TEST_STAKE)
        
    def test_stake_not_set(self):
        with self.assertRaises(ValueError):
            self.stakeHanlder.get_stake()
            
    def test_check_cards_two_pair(self):
        self.stakeHanlder.set_stake(self.TEST_TWO_PAIR)
        self.assertTrue(self.stakeHanlder.check_cards(self.TEST_TWO_PAIR_CARDS))
        
    def test_check_invalid_cards_two_pair(self):
        self.stakeHanlder.set_stake(self.TEST_TWO_PAIR)
        self.assertFalse(self.stakeHanlder.check_cards(self.TEST_INVALID_TWO_PAIR_CARDS))
            
    def test_check_cards_royal_flush(self):
        self.stakeHanlder.set_stake(self.TEST_ROYAL_FLUSH)
        self.assertTrue(self.stakeHanlder.check_cards(self.TEST_ROYAL_FLUSH_CARDS))
        
    def test_check__invalid_cards_royal_flush(self):
        self.stakeHanlder.set_stake(self.TEST_ROYAL_FLUSH)
        self.assertFalse(self.stakeHanlder.check_cards(self.TEST_INVALID_ROYAL_FLUSH_CARDS))


if __name__ == "__main__":
    unittest.main()
