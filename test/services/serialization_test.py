import json
import unittest

from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.player import Player
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.services.deserialize.impl import Deserializer
from src.services.message import Message
from src.services.serialize.impl import Serializer

class SerializeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_player1 = Player("Player1")
        test_player1.cards = [
            Card(Suit.SPADES, Rank.TWO),
        ]
        test_player2 = Player("Player2")
        test_player2.cards_in_hand = 2
        cls.TEST_MESSAGE = Message(
            {
                "players": [test_player1, test_player2],
                "stake": Stake(
                    Combination.STRAIGHT_FLUSH,
                    [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE],
                    Suit.SPADES),
            })
        cls.TEST_SERIALIZED_MESSAGE = """
        {
            "body": {
                "players": [
                {
                    "username": "Player1",
                    "cards": [
                        {
                            "suit": {
                                "name": "SPADES",
                                "$type": "Suit"
                            },
                            "rank": {
                                "name": "TWO",
                                "$type": "Rank"
                            },
                            "$type": "Card"
                        }
                    ],
                    "cards_in_hand": 0,
                    "$type": "Player"
                },
                {
                    "username": "Player2",
                    "cards": [],
                    "cards_in_hand": 2,
                    "$type": "Player"
                }
                ],
                "stake": {
                    "ranks": [
                        {
                        "name": "ONE",
                        "$type": "Rank"
                        },
                        {
                        "name": "TWO",
                        "$type": "Rank"
                        },
                        {
                        "name": "THREE",
                        "$type": "Rank"
                        },
                        {
                        "name": "FOUR",
                        "$type": "Rank"
                        },
                        {
                        "name": "FIVE",
                        "$type": "Rank"
                        }
                    ],
                    "suits": [
                        {
                        "name": "SPADES",
                        "$type": "Suit"
                        }
                    ],
                    "combo": {
                        "name": "STRAIGHT_FLUSH",
                        "$type": "Combination"
                    },
                    "$type": "Stake"
                }
            },
            "$type": "Message"
        }"""

    def setUp(self):
        self.serializer = Serializer()
        self.deserializer = Deserializer()

    def test_serialize(self):
        actual = json.loads(self.serializer.serialize(self.TEST_MESSAGE))
        expected = json.loads(self.TEST_SERIALIZED_MESSAGE)
        self.assertEqual(actual, expected)
    
    def test_deserialize(self):
        actual = self.deserializer.deserialize(self.TEST_SERIALIZED_MESSAGE)
        expected = self.TEST_MESSAGE
        self.assertEqual(actual, expected)
        
    def test_serialize_deserialize(self):
        serialized = self.serializer.serialize(self.TEST_MESSAGE)
        deserialized = self.deserializer.deserialize(serialized)
        self.assertEqual(self.TEST_MESSAGE, deserialized)
        