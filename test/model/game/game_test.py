import unittest
from src.model.deck import Card
from src.model.deck.suit import Suit
from src.model.stake import Combination
from src.model.stake import Stake
from src.model.player import Player
from src.model.game.impl import GameImpl


class TestGameImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_PLAYER_1 = Player("Bob", [], 0)
        cls.TEST_PLAYER_2 = Player("Lisa", [], 0)
        cls.TEST_PLAYERS = [Player("Bob", [], 0), Player("Lisa", [], 0), Player("John", [], 0)]
        cls.TEST_STAKE = Stake([2, 5], Combination.TWO_PAIR)
        cls.TEST_STAKES = [Stake([2, 5], Combination.TWO_PAIR), Stake([], Combination.THREE_OF_A_KIND), Stake([], Combination.FULL_HOUSE), Stake([], Combination.FOUR_OF_A_KIND)]

    def setUp(self):
        self.game = GameImpl()
    
    def test_cannot_start_without_enough_players(self):
        self.game.addPlayer(self.TEST_PLAYER_1)
        with self.assertRaises(ValueError) as context:
            self.game.startTurn()
        self.assertEqual(str(context.exception), "Cannot start without enough players")
    
    def addTwoPlayers(self):
        self.game.addPlayer(self.TEST_PLAYER_1)
        self.game.addPlayer(self.TEST_PLAYER_2)

    def test_players_have_one_card_at_the_beginning(self):
        self.addTwoPlayers()
        self.game.startTurn()
        self.assertEqual(self.game.STARTING_CARDS, self.TEST_PLAYER_1.cardsInHand)
        self.assertEqual(self.game.STARTING_CARDS, self.TEST_PLAYER_2.cardsInHand)
    
    def test_first_player_is_the_first_added(self):
        self.addTwoPlayers()
        self.game.startTurn()
        self.assertEqual(self.TEST_PLAYER_1, self.game.getCurrentPlayer())
    
    def test_current_player_can_raise_the_stake(self):
        self.addTwoPlayers()
        self.game.startTurn()
        self.game.raiseStake(self.TEST_STAKE)
        self.assertEqual(self.TEST_STAKE, self.game.getLatestStake())
    
    def test_check_liar_is_false(self):
        self.game.addPlayer(Player("Pippo", [Card(Suit.HEARTS, 1), Card(Suit.SPADES, 1), Card(Suit.HEARTS, 5)], 3))
        self.game.addPlayer(Player("Laura", [Card(Suit.CLUBS, 6), Card(Suit.DIAMONDS, 1)], 2))
        self.game.raiseStake(self.TEST_STAKE)
        self.assertFalse(self.game.checkLiar())
    
    def test_cycle_of_players_in_the_turn(self):
        for player in self.TEST_PLAYERS:
            self.game.addPlayer(player)
        self.game.startTurn()
        for i in range(len(self.TEST_PLAYERS)):
            self.game.raiseStake(self.TEST_STAKES[i])
        self.assertEqual(self.TEST_PLAYERS[0], self.game.getCurrentPlayer())





if __name__ == "__main__":
    unittest.main()

