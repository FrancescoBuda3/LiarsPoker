from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
   SART_GAME = "start_game"
   START_ROUND = "start_round"
   START_TURN = "start_turn"
   ROUNT_LOSER = "round_loser"
   SHOW_CARDS = "show_cards"
   ELIMINATION = "elimination"
   GAME_OVER = "game_over"

@dataclass
class Message:
    """
    A container for a request to the server. 
    """

    header: str
    body: object