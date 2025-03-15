import unittest
from src.model.deck import Card
from src.model.deck.suit import Suit
from src.model.stake import Combination
from src.model.stake import Stake
from src.model.player import Player
from src.model.game.impl import GameCore


class TestGameCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_PLAYER_1 = Player("Bob")
        cls.TEST_PLAYER_2 = Player("Lisa")
        cls.TEST_PLAYERS = [Player("Bob"), Player("Lisa"), Player("John")]
        cls.TEST_STAKE = Stake(Combination.TWO_PAIR, [2, 5])
        cls.TEST_STAKES = [Stake(Combination.TWO_PAIR, [2, 5]), Stake(Combination.THREE_OF_A_KIND, [3]), Stake(Combination.FULL_HOUSE, [1,3], []), Stake(Combination.FOUR_OF_A_KIND, [5])]

    def setUp(self):
        self.game = GameCore()
    
    def test_cannot_start_without_enough_players(self):
        self.game.add_player(self.TEST_PLAYER_1)
        with self.assertRaises(ValueError) as context:
            self.game.start_game()
        self.assertEqual(str(context.exception), "Cannot start without enough players")
    
    def addTwoPlayers(self):
        self.game.add_player(self.TEST_PLAYER_1)
        self.game.add_player(self.TEST_PLAYER_2)

    def test_players_have_one_card_at_the_beginning(self):
        self.addTwoPlayers()
        self.game.start_round()
        self.assertEqual(self.game.STARTING_CARDS, self.TEST_PLAYER_1.cards_in_hand)
        self.assertEqual(self.game.STARTING_CARDS, self.TEST_PLAYER_2.cards_in_hand)
    
    def test_first_player_is_the_first_added(self):
        self.addTwoPlayers()
        self.game.start_round()
        self.assertEqual(self.TEST_PLAYER_1, self.game.get_current_player())
    
    def test_current_player_can_raise_the_stake(self):
        self.addTwoPlayers()
        self.game.start_round()
        self.game.raise_stake(self.TEST_STAKE)
        self.assertEqual(self.TEST_STAKE, self.game.get_latest_stake())
    
    def test_check_liar(self):
        p1 = Player("Pippo")
        p1.cards = [Card(Suit.HEARTS, 1), Card(Suit.SPADES, 1), Card(Suit.HEARTS, 5)]
        p1.cards_in_hand = 3
        p2 = Player("Laura")
        p2.cards = [Card(Suit.CLUBS, 6), Card(Suit.DIAMONDS, 1)]
        p2.cards_in_hand = 2
        self.game.add_player(p1)
        self.game.add_player(p2)
        self.game.raise_stake(self.TEST_STAKE)
        self.assertTrue(self.game.check_liar())
    
    def test_cycle_of_players_in_the_turn(self):
        for player in self.TEST_PLAYERS:
            self.game.add_player(player)
        self.game.start_round()
        for i in range(len(self.TEST_PLAYERS)):
            self.game.raise_stake(self.TEST_STAKES[i])
        self.assertEqual(self.TEST_PLAYERS[0], self.game.get_current_player())

    def test_loser_is_the_first_in_next_turn(self):
        p1 = Player("Pippo")
        p1.cards = [Card(Suit.HEARTS, 1), Card(Suit.SPADES, 1), Card(Suit.HEARTS, 5)]
        p1.cards_in_hand = 3
        p2 = Player("Laura")
        p2.cards = [Card(Suit.CLUBS, 6), Card(Suit.DIAMONDS, 1)]
        p2.cards_in_hand = 2
        self.game.add_player(p1)
        self.game.add_player(p2)
        self.game.raise_stake(Stake(Combination.HIGH_CARD, [1]))
        self.game.raise_stake(Stake(Combination.FLUSH))
        self.game.check_liar()
        self.assertEqual(p2, self.game.get_current_player())






if __name__ == "__main__":
    unittest.main()

