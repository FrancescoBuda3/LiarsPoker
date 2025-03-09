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
        cls.TEST_PLAYER_1 = Player("Bob", [], 0)
        cls.TEST_PLAYER_2 = Player("Lisa", [], 0)
        cls.TEST_PLAYERS = [Player("Bob", [], 0), Player("Lisa", [], 0), Player("John", [], 0)]
        cls.TEST_STAKE = Stake([2, 5], Combination.TWO_PAIR)
        cls.TEST_STAKES = [Stake([2, 5], Combination.TWO_PAIR), Stake([], Combination.THREE_OF_A_KIND), Stake([], Combination.FULL_HOUSE), Stake([], Combination.FOUR_OF_A_KIND)]

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
        self.assertEqual(self.game.STARTING_CARDS, self.TEST_PLAYER_1.cardsInHand)
        self.assertEqual(self.game.STARTING_CARDS, self.TEST_PLAYER_2.cardsInHand)
    
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
        self.game.add_player(Player("Pippo", [Card(Suit.HEARTS, 1), Card(Suit.SPADES, 1), Card(Suit.HEARTS, 5)], 3))
        self.game.add_player(Player("Laura", [Card(Suit.CLUBS, 6), Card(Suit.DIAMONDS, 1)], 2))
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
        player1 = Player("Pippo", [Card(Suit.HEARTS, 1), Card(Suit.SPADES, 1), Card(Suit.HEARTS, 5)], 3)
        player2 = Player("Laura", [Card(Suit.CLUBS, 6), Card(Suit.DIAMONDS, 1)], 2)
        self.game.add_player(player1)
        self.game.add_player(player2)
        self.game.raise_stake(Stake([1], Combination.HIGH_CARD))
        self.game.raise_stake(Stake([], Combination.FLUSH))
        self.game.check_liar()
        self.assertEqual(player2, self.game.get_current_player())






if __name__ == "__main__":
    unittest.main()

