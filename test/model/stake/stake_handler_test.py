import unittest
from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.model.stake.impl import StakeHandlerImpl


class TestStakeHandlerImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_STAKE = Stake(Combination.HIGH_CARD, [Rank.ONE])
        cls.TEST_NEXT_STAKE = Stake(Combination.HIGH_CARD, [Rank.TWO])
        cls.TEST_TWO_PAIR = Stake(Combination.TWO_PAIR, [Rank.FIVE, Rank.TWO])
        cls.TEST_NEXT_TWO_PAIR = Stake(Combination.TWO_PAIR, [Rank.FIVE, Rank.THREE])
        cls.TEST_TWO_PAIR_CARDS = [
            Card(Suit.SPADES, Rank.TWO), 
            Card(Suit.HEARTS, Rank.TWO), 
            Card(Suit.SPADES, Rank.FIVE), 
            Card(Suit.HEARTS, Rank.FIVE)]
        cls.TEST_INVALID_TWO_PAIR_CARDS = [
            Card(Suit.SPADES, Rank.TWO), 
            Card(Suit.HEARTS, Rank.FIVE), 
            Card(Suit.SPADES, Rank.FIVE)]
        cls.TEST_ROYAL_FLUSH = Stake(Combination.ROYAL_FLUSH, suits=Suit.SPADES)
        cls.TEST_ROYAL_FLUSH_CARDS = [
            Card(Suit.SPADES, Rank.TEN), 
            Card(Suit.SPADES, Rank.JACK), 
            Card(Suit.SPADES, Rank.QUEEN), 
            Card(Suit.SPADES, Rank.KING), 
            Card(Suit.SPADES, Rank.ACE)]
        cls.TEST_INVALID_ROYAL_FLUSH_CARDS = [
            Card(Suit.SPADES, Rank.TEN), 
            Card(Suit.SPADES, Rank.JACK), 
            Card(Suit.SPADES, Rank.QUEEN), 
            Card(Suit.SPADES, Rank.KING), 
            Card(Suit.SPADES, Rank.TWO)]
        cls.TEST_STRAIGHT_FLUSH_SPADES = Stake(
            Combination.STRAIGHT_FLUSH, 
            [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE], 
            Suit.SPADES)
        cls.TEST_STRAIGHT_FLUSH_HEARTS = Stake(
            Combination.STRAIGHT_FLUSH, 
            [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE], 
            Suit.HEARTS)
        cls.TEST_HIGHEST_CARD = Stake(Combination.HIGH_CARD, [Rank.ACE])
        cls.TEST_LOWEST_PAIR = Stake(Combination.PAIR, [Rank.ONE])

    def setUp(self):
        self.stakeHandler = StakeHandlerImpl()

    def test_stake(self):
        self.stakeHandler.stake = self.TEST_STAKE
        self.assertEqual(self.stakeHandler.stake, self.TEST_STAKE)

    def test_reset_stake(self):
        self.stakeHandler.stake = self.TEST_STAKE
        self.stakeHandler.reset_stake()
        with self.assertRaises(ValueError):
            self.stakeHandler.stake

    def test_stake_not_set(self):
        with self.assertRaises(ValueError):
            self.stakeHandler.stake

    def test_check_state_not_set(self):
        with self.assertRaises(ValueError):
            self.stakeHandler.check_cards([])

    def test_check_cards_two_pair(self):
        self.stakeHandler.stake = self.TEST_TWO_PAIR
        self.assertTrue(self.stakeHandler.check_cards(
            self.TEST_TWO_PAIR_CARDS))

    def test_check_invalid_cards_two_pair(self):
        self.stakeHandler.stake = self.TEST_TWO_PAIR
        self.assertFalse(self.stakeHandler.check_cards(
            self.TEST_INVALID_TWO_PAIR_CARDS))

    def test_check_cards_royal_flush(self):
        self.stakeHandler.stake = self.TEST_ROYAL_FLUSH
        self.assertTrue(self.stakeHandler.check_cards(
            self.TEST_ROYAL_FLUSH_CARDS))

    def test_check__invalid_cards_royal_flush(self):
        self.stakeHandler.stake = self.TEST_ROYAL_FLUSH
        self.assertFalse(self.stakeHandler.check_cards(
            self.TEST_INVALID_ROYAL_FLUSH_CARDS))

    def test_get_lowest_next_stake(self):
        self.stakeHandler.stake = self.TEST_STAKE
        self.assertEqual(
            self.stakeHandler.get_lowest_next_stake(), self.TEST_NEXT_STAKE)

    def test_get_lowest_next_stake_two_pair(self):
        self.stakeHandler.stake = self.TEST_TWO_PAIR
        self.assertEqual(
            self.stakeHandler.get_lowest_next_stake(), self.TEST_NEXT_TWO_PAIR)

    def test_get_lowest_next_stake_royal_flush(self):
        self.stakeHandler.stake = self.TEST_ROYAL_FLUSH
        self.assertNotEqual(
            self.stakeHandler.get_lowest_next_stake().suit, self.TEST_ROYAL_FLUSH.suit)

    def test_different_suit_straight_flush(self):
        self.stakeHandler.stake = self.TEST_STRAIGHT_FLUSH_SPADES
        self.stakeHandler.stake = self.stakeHandler.get_lowest_next_stake()
        self.assertTrue(
            self.TEST_STRAIGHT_FLUSH_HEARTS.suit in self.stakeHandler.stake.suits and
            self.TEST_STRAIGHT_FLUSH_SPADES.ranks == self.stakeHandler.stake.ranks
        )

    def test_multiple_suits_royal_flush(self):
        self.stakeHandler.stake = self.TEST_ROYAL_FLUSH
        self.stakeHandler.stake = self.stakeHandler.get_lowest_next_stake()
        self.stakeHandler.stake = self.stakeHandler.get_lowest_next_stake()
        self.stakeHandler.stake = self.stakeHandler.get_lowest_next_stake()
        self.assertEqual(
            self.stakeHandler.get_lowest_next_stake(), None)
        
    def test_highest_card(self):
        self.stakeHandler.stake = self.TEST_HIGHEST_CARD
        self.assertEqual(
            self.stakeHandler.get_lowest_next_stake(), self.TEST_LOWEST_PAIR)


if __name__ == "__main__":
    unittest.main()
