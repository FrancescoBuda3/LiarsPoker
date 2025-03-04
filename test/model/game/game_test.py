import unittest
from src.model.player import Player
from src.model.game.impl import GameImpl


class TestGameImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testPlayer1 = Player("Bob", [], 0)
        cls.testPlayer2 = Player("Lisa", [], 0)
        cls.starting_hand_size = 1

    def setUp(self):
        self.game = GameImpl()
    
    def test_doesnt_start_without_players(self):
        with self.assertRaises(ValueError) as context:
            self.game.startTurn()
        self.assertEqual(str(context.exception), "Cannot start without players")
    
    def test_players_have_one_card_at_the_beginning(self):
        self.game.addPlayer(self.testPlayer1)
        self.game.addPlayer(self.testPlayer2)
        self.game.startTurn()
        self.assertEqual(self.starting_hand_size, self.testPlayer1.cardsInHand)
        self.assertEqual(self.starting_hand_size, self.testPlayer2.cardsInHand)

if __name__ == "__main__":
    unittest.main()

