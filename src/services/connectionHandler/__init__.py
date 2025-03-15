from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    CARDS = "cards"
    PLAYER_TURN = "player_turn"
    STAKE = "stake"
    LIE = "lie"
    LOSER = "loser"
    WINNER = "winner"


@dataclass
class Message():
    message_type: MessageType
    body: str


class ConnectionHandler():
    def send_message(self, message: Message):
        """
        sends a message to all the listeners
        Args:
            message (Message): message to send
        """
        pass
    
    def wait_message(self, timeout=None) -> Message:
        """
        waits for a message to be received
        Args:
            timeout (int): maximum time to wait for a message, if none waits indefinitely
        Returns:
            Message: message received
        """
        pass
