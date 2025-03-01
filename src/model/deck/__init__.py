from dataclasses import dataclass

@dataclass
class Card():
    def __post_init__(self):
        raise NotImplementedError("Card not implemented")