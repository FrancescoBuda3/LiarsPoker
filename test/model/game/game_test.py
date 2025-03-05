import unittest
from src.model.stake import Combination
from src.model.stake import Stake
from src.model.player import Player
from src.model.game.impl import GameImpl


class TestGameImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_PLAYER_1 = Player("Bob", [], 0)
        cls.TEST_PLAYER_2 = Player("Lisa", [], 0)
        cls.TEST_STAKE = Stake([2, 5], Combination.TWO_PAIR)

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
        player = self.game.getCurrentPlayer()
        self.game.raiseStake(self.TEST_STAKE)
        self.assertEqual(self.TEST_STAKE, self.game.getLatestStake())



if __name__ == "__main__":
    unittest.main()

