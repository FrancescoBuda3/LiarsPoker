from dataclasses import dataclass
import json

from src.model.player import Player

@dataclass
class Message:
    """
    A container for a request to the server. 
    """

    header: str
    body: object
