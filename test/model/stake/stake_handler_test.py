import unittest
from src.model.deck import Card
from src.model.deck.suit import Suit
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.model.stake.impl import StakeHandlerImpl


class TestStakeHandlerImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_STAKE = Stake(Combination.HIGH_CARD, [1])
        cls.TEST_NEXT_STAKE = Stake(Combination.HIGH_CARD, [2])
        cls.TEST_TWO_PAIR = Stake(Combination.TWO_PAIR, [2, 5])
        cls.TEST_NEXT_TWO_PAIR = Stake(Combination.TWO_PAIR, [5, 3])
        cls.TEST_TWO_PAIR_CARDS = [Card(Suit.SPADES, 2), Card(
            Suit.HEARTS, 2), Card(Suit.SPADES, 5), Card(Suit.HEARTS, 5)]
        cls.TEST_INVALID_TWO_PAIR_CARDS = [
            Card(Suit.SPADES, 2), Card(Suit.HEARTS, 5), Card(Suit.SPADES, 5)]
        cls.TEST_ROYAL_FLUSH = Stake(Combination.ROYAL_FLUSH, suits=Suit.SPADES)
        cls.TEST_ROYAL_FLUSH_CARDS = [Card(Suit.SPADES, 10), Card(Suit.SPADES, 11), Card(
            Suit.SPADES, 12), Card(Suit.SPADES, 13), Card(Suit.SPADES, 14)]
        cls.TEST_INVALID_ROYAL_FLUSH_CARDS = [Card(Suit.SPADES, 10), Card(
            Suit.SPADES, 11), Card(Suit.SPADES, 12), Card(Suit.SPADES, 13), Card(Suit.SPADES, 2)]
        cls.TEST_STRAIGHT_FLUSH_SPADES = Stake(
            Combination.STRAIGHT_FLUSH, [1, 2, 3, 4, 5], Suit.SPADES)
        cls.TEST_STRAIGHT_FLUSH_HEARTS = Stake(
            Combination.STRAIGHT_FLUSH, [1, 2, 3, 4, 5], Suit.HEARTS)

    def setUp(self):
        self.stakeHanlder = StakeHandlerImpl()

    def test_stake(self):
        self.stakeHanlder.stake = self.TEST_STAKE
        self.assertEqual(self.stakeHanlder.stake, self.TEST_STAKE)

    def test_reset_stake(self):
        self.stakeHanlder.stake = self.TEST_STAKE
        self.stakeHanlder.reset_stake()
        with self.assertRaises(ValueError):
            self.stakeHanlder.stake

    def test_stake_not_set(self):
        with self.assertRaises(ValueError):
            self.stakeHanlder.stake

    def test_check_state_not_set(self):
        with self.assertRaises(ValueError):
            self.stakeHanlder.check_cards([])

    def test_check_cards_two_pair(self):
        self.stakeHanlder.stake = self.TEST_TWO_PAIR
        self.assertTrue(self.stakeHanlder.check_cards(
            self.TEST_TWO_PAIR_CARDS))

    def test_check_invalid_cards_two_pair(self):
        self.stakeHanlder.stake = self.TEST_TWO_PAIR
        self.assertFalse(self.stakeHanlder.check_cards(
            self.TEST_INVALID_TWO_PAIR_CARDS))

    def test_check_cards_royal_flush(self):
        self.stakeHanlder.stake = self.TEST_ROYAL_FLUSH
        self.assertTrue(self.stakeHanlder.check_cards(
            self.TEST_ROYAL_FLUSH_CARDS))

    def test_check__invalid_cards_royal_flush(self):
        self.stakeHanlder.stake = self.TEST_ROYAL_FLUSH
        self.assertFalse(self.stakeHanlder.check_cards(
            self.TEST_INVALID_ROYAL_FLUSH_CARDS))

    def test_get_lowest_next_stake(self):
        self.stakeHanlder.stake = self.TEST_STAKE
        self.assertEqual(
            self.stakeHanlder.get_lowest_next_stake(), self.TEST_NEXT_STAKE)

    def test_get_lowest_next_stake_two_pair(self):
        self.stakeHanlder.stake = self.TEST_TWO_PAIR
        self.assertEqual(
            self.stakeHanlder.get_lowest_next_stake(), self.TEST_NEXT_TWO_PAIR)

    def test_get_lowest_next_stake_royal_flush(self):
        self.stakeHanlder.stake = self.TEST_ROYAL_FLUSH
        self.assertNotEqual(
            self.stakeHanlder.get_lowest_next_stake().suit, self.TEST_ROYAL_FLUSH.suit)
        
    def test_different_suit_straight_flush(self):
        self.stakeHanlder.stake = self.TEST_STRAIGHT_FLUSH_SPADES
        self.stakeHanlder.stake = self.stakeHanlder.get_lowest_next_stake()
        self.assertTrue(
            self.TEST_STRAIGHT_FLUSH_HEARTS.suit in self.stakeHanlder.stake.suits and
            self.TEST_STRAIGHT_FLUSH_SPADES.ranks == self.stakeHanlder.stake.ranks
        )

    def test_multiple_suits_royal_flush(self):
        self.stakeHanlder.stake = self.TEST_ROYAL_FLUSH
        self.stakeHanlder.stake = self.stakeHanlder.get_lowest_next_stake()
        self.stakeHanlder.stake = self.stakeHanlder.get_lowest_next_stake()
        self.stakeHanlder.stake = self.stakeHanlder.get_lowest_next_stake()
        self.assertEqual(
            self.stakeHanlder.get_lowest_next_stake(), None)


if __name__ == "__main__":
    unittest.main()
