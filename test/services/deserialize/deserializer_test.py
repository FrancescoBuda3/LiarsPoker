import unittest

from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.player import Player
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.services.deserialize.impl import Deserializer
from src.services.message import Message


class DeserializeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_string_1 = '{"$type": "Message", "header": "start_round", "body": { "player_order": [ { "$type": "Player", "username": "GinoPino", "cards": [], "cards_in_hand": 0 }, { "$type": "Player", "username": "CippaLippa", "cards": [], "cards_in_hand": 0 } ] } }'
        cls.test_header_1 = "start_round"
        cls.test_obj_1 = {"player_order": [Player("GinoPino"), Player("CippaLippa")]}
        cls.test_string_2 = '{"$type": "Stake", "combo": "THREE_OF_A_KIND", "ranks": ["KING", "QUEEN", "ONE" ], "suits": [ "HEARTS"] }'
        cls.test_obj_2 = Stake(Combination.THREE_OF_A_KIND, [Rank.KING, Rank.QUEEN, Rank.ONE], [Suit.HEARTS])

    def setUp(self):
        self.deserializer = Deserializer()
    
    def test_deserialize(self):
        self.assertEqual(self.deserializer.deserialize(self.test_string_1), Message(self.test_header_1, self.test_obj_1))
        print(self.deserializer.deserialize(self.test_string_2))
        self.assertEqual(self.deserializer.deserialize(self.test_string_2), self.test_obj_2)