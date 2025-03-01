from dataclasses import dataclass

@dataclass
class User():
    username: str
    address: tuple[str, int]

    def __post_init__(self):
        if not self.username:
            raise ValueError("Username is required")
        if not self.address:
            raise ValueError("Address is required")