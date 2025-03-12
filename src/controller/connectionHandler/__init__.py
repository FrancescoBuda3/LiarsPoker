from enum import Enum

class MessageType(Enum):
    CARDS: "cards"
    PLAYER_TURN: "player_turn"
    STAKE: "stake"
    BULLSH*T: "bullsh*t"
    LOSER: "loser"
    WINNER: "winner"


@dataclass
class Message():
    message_type: MessageType
    body: str


class ConnectionHandler():
    def send_message(self, message: Message):
        """
        Args:
            message (Message): message to send
        """
        pass
    
    def wait_message(self) -> Message:
        """
        Returns:
            Message: message received
        """
        pass
