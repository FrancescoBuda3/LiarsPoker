from dataclasses import dataclass

@dataclass
class Message:
    """
    A container for a request to the server. 
    """

    header: str
    body: object
