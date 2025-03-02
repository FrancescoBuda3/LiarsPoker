import unittest
from src.model.game.impl import GameImpl


class TestGameImpl(unittest.TestCase):
    def setUp(self):
        self.game = GameImpl()
    
    def test_initial_state(self):
        self.assertEqual(self.game._debug, True)

if __name__ == "__main__":
    unittest.main()
