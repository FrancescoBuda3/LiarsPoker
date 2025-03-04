import unittest
from src.model.player import Player
from src.model.game.impl import GameImpl


class TestGameImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_PLAYER_1 = Player("Bob", [], 0)
        cls.TEST_PLAYER_2 = Player("Lisa", [], 0)

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


if __name__ == "__main__":
    unittest.main()

