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
        cls.TEST_SUIT = Suit.SPADES
        cls.TEST_ONE_STAKE = Stake(Combination.HIGH_CARD, [Rank.ONE])
        cls.TEST_FULL_HOUSE = Stake(Combination.FULL_HOUSE)
        cls.TEST_FULL_HOUSE.triple_rank = Rank.TWO
        cls.TEST_FULL_HOUSE.pair_rank = Rank.THREE
        cls.TEST_STRAIGHT_FLUSH = Stake(Combination.STRAIGHT_FLUSH)
        cls.TEST_STRAIGHT_FLUSH.ranks = [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX]
        cls.TEST_STRAIGHT_FLUSH.suit = Suit.SPADES
        cls.TEST_ROYAL_FLUSH = Stake(Combination.ROYAL_FLUSH)
        cls.TEST_ROYAL_FLUSH.suit = Suit.SPADES

    def setUp(self):
        self.stakeHandler = StakeHandlerImpl()

    def test_stake(self):
        self.stakeHandler.stake = self.TEST_ONE_STAKE
        self.assertEqual(self.stakeHandler.stake, self.TEST_ONE_STAKE)

    def test_reset_stake(self):
        self.stakeHandler.stake = self.TEST_ONE_STAKE
        self.stakeHandler.reset_stake()
        self.assertIsNone(self.stakeHandler.stake)

    def test_stake_not_set(self):
        self.assertIsNone(self.stakeHandler.stake)

    def test_check_state_not_set(self):
        with self.assertRaises(ValueError):
            self.stakeHandler.check_cards([])

    def test_check_full_house(self):
        self.stakeHandler.stake = self.TEST_FULL_HOUSE
        full_house_cards = []
        for i in range(3):
            full_house_cards.append(
                Card(self.TEST_SUIT, self.TEST_FULL_HOUSE.triple_rank))
        for i in range(2):
            full_house_cards.append(
                Card(self.TEST_SUIT, self.TEST_FULL_HOUSE.pair_rank))
        self.assertTrue(self.stakeHandler.check_cards(full_house_cards))

    def test_check_wrong_full_house(self):
        self.stakeHandler.stake = self.TEST_FULL_HOUSE
        wrong_full_house_cards = []
        for i in range(3):
            wrong_full_house_cards.append(
                Card(self.TEST_SUIT, self.TEST_FULL_HOUSE.pair_rank))
        for i in range(2):
            wrong_full_house_cards.append(
                Card(self.TEST_SUIT, self.TEST_FULL_HOUSE.triple_rank))
        self.assertFalse(self.stakeHandler.check_cards(wrong_full_house_cards))

    def test_check_straight_flush(self):
        self.stakeHandler.stake = self.TEST_STRAIGHT_FLUSH
        straight_flush_cards = []
        for i in range(5):
            straight_flush_cards.append(
                Card(self.TEST_STRAIGHT_FLUSH.suit, self.TEST_STRAIGHT_FLUSH.ranks[i]))
        self.assertTrue(self.stakeHandler.check_cards(straight_flush_cards))

    def test_check_wrong_straight_flush(self):
        self.stakeHandler.stake = self.TEST_STRAIGHT_FLUSH
        straight_flush_cards = []
        for i in range(4):
            straight_flush_cards.append(
                Card(self.TEST_STRAIGHT_FLUSH.suit, self.TEST_STRAIGHT_FLUSH.ranks[i]))
        self.assertFalse(self.stakeHandler.check_cards(straight_flush_cards))

    def test_get_lowest_next_stake(self):
        self.stakeHandler.stake = self.TEST_ONE_STAKE
        next_stake = Stake(self.TEST_ONE_STAKE.combo)
        next_stake.ranks = [Rank.TWO]
        self.assertEqual(
            self.stakeHandler.get_lowest_next_stake(), next_stake)

    def test_get_lowest_next_stake_full_house(self):
        self.stakeHandler.stake = self.TEST_FULL_HOUSE
        next_stake = Stake(self.TEST_FULL_HOUSE.combo)
        next_stake.ranks = [Rank.FOUR, Rank.THREE]
        self.assertEqual(
            self.stakeHandler.get_lowest_next_stake(), next_stake)

    def test_get_lowest_next_stake_royal_flush(self):
        self.stakeHandler.stake = self.TEST_ROYAL_FLUSH
        next_stake = Stake(self.TEST_ROYAL_FLUSH.combo)
        next_stake.suits = [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]
        self.assertEqual(
            self.stakeHandler.get_lowest_next_stake(), next_stake)
        
    def test_highest_card(self):
        self.stakeHandler.stake = Stake(Combination.HIGH_CARD, [Rank.ACE])
        next_stake = Stake(Combination.PAIR, [Rank.ONE])
        self.assertEqual(
            self.stakeHandler.get_lowest_next_stake(), next_stake)


if __name__ == "__main__":
    unittest.main()
