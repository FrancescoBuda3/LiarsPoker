import unittest
from src.model.game.GImpl import GameImpl, GamePhase
from src.model.player import Player


class TestGameImpl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.TEST_PLAYERS = [
            Player("Alice", 1), 
            Player("Bob", 2), 
            Player("Charlie", 3), 
            Player("David", 4)]

    def setUp(self):
        self.game = GameImpl()

    def add_players(self):
        for player in self.TEST_PLAYERS:
            self.game.add_player(player)

    def test_can_add_player_while_waiting_for_players(self):
        self.add_players()
        self.assertEqual(len(self.TEST_PLAYERS), len(self.game.get_players()))

    def test_cannot_add_player_while_game_running(self):
        self.add_players()
        self.game.start_game()
        with self.assertRaises(ValueError):
            self.game.add_player(Player("Bob", 5))

    def test_cannot_start_round_before_game_started(self):
        with self.assertRaises(ValueError):
            self.game.start_round()

    def test_cannot_rise_stake_before_round_started(self):
        self.add_players()
        self.game.start_game()
        with self.assertRaises(ValueError):
            self.game.raise_stake(1)

    def test_cannot_check_liar_before_round_started(self):
        self.add_players()
        self.game.start_game()
        with self.assertRaises(ValueError):
            self.game.check_liar()

    def test_can_remove_player_while_waiting_for_players(self):
        self.add_players()
        self.game.remove_player(self.TEST_PLAYERS[0])
        self.assertEqual(len(self.TEST_PLAYERS) - 1,
                         len(self.game.get_players()))

    def test_can_remove_player_while_it_is_their_turn(self):
        self.add_players()
        self.game.start_game()
        self.game.start_round()
        self.game.remove_player(self.TEST_PLAYERS[0])
        self.assertEqual(len(self.TEST_PLAYERS) - 1,
                         len(self.game.get_players()))

    def test_game_over_when_only_one_player_left(self):
        self.add_players()
        self.game.start_game()
        for i in range(len(self.TEST_PLAYERS) - 1):
            self.game.start_round()
            self.game.remove_player(self.TEST_PLAYERS[i])
        self.assertEqual(1, len(self.game.get_players()))
        self.assertEqual(GamePhase.GAME_OVER, self.game.get_phase())


if __name__ == "__main__":
    unittest.main()
