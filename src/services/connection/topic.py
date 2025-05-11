from enum import Enum


class Topic(str, Enum):
    LOBBY = "lobby"
    NEW_LOBBY = "new_lobby"
    NEW_PLAYER = "new_player"
    NEW_GAME = "new_game"
    JOIN_LOBBY = "join_lobby"
    DISCONNECT_PLAYER = "disconnect_player"
    LEAVE_LOBBY = "leave_lobby"
    DELETE_LOBBY = "delete_lobby"
    SHOW_CARDS = "show_cards"
    START_TURN = "start_turn"
    START_ROUND = "start_round"
    ROUND_LOSER = "round_loser"
    ELIMINATION = "elimination"
    GAME_OVER = "game_over"
    RAISE_STAKE = "raise_stake"
    CHECK_LIAR = "check_liar"
    
    def __add__(self, other: str) -> str:
        """
        Returns:
            str: "topic/other"
        """
        return f"{self.value}/{other}"
    
    def __radd__(self, other: str) -> str:
        """
        Returns:
            str: "other/topic"
        """
        return f"{other}/{self.value}"
    
game_topics = [
    Topic.SHOW_CARDS,
    Topic.START_TURN,
    Topic.START_ROUND,
    Topic.ROUND_LOSER,
    Topic.ELIMINATION,
    Topic.RAISE_STAKE,
    Topic.CHECK_LIAR,
    Topic.GAME_OVER,
]