import unittest
import sys  
sys.path.append("./")
from src.model.deck.impl import DeckImpl


class TestDeckImpl(unittest.TestCase):
    def setUp(self):
        self.deck = DeckImpl()
    
    def test_initial_state(self):
        self.assertEqual(len(self.deck.cards), 52)
        
    def test_shuffle(self):
        hands = [5, 5, 5, 5]
        hands = self.deck.shuffle(hands)
        self.assertEqual(len(hands), 4)
        self.assertEqual(len(hands[0]), 5)
        self.assertEqual(len(hands[1]), 5)
        self.assertEqual(len(hands[2]), 5)
        self.assertEqual(len(hands[3]), 5)
        self.assertEqual(len(self.deck.cards), 32)

if __name__ == "__main__":
    unittest.main()
