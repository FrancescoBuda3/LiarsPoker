from dataclasses import dataclass
from enum import Enum

class Header(Enum):
    SHOW_CARDS = "show_cards"
    START_TURN = "start_turn"
    START_ROUND = "start_round"
    ROUND_LOSER = "round_loser"
    ELIMINATION = "elimination"
    GAME_OVER = "game_over"

@dataclass
class Message:
    """
    A container for a request to the server. 
    """

    header: str
    body: object