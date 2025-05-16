from dataclasses import dataclass

@dataclass
class Message:
    """
    A container for simple messages with only a body. 
    """
    body: dict