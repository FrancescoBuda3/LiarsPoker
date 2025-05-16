import uuid


class __UserState:
    username: str
    selected_lobby: int
    id: uuid.UUID
    
    def __init__(self):
        self.username = ''
        self.selected_lobby = 0
        self.id = uuid.uuid4()

    def __str__(self):
        return f"username={self.username}, selected_lobby={self.selected_lobby}"
    
    def reset(self):
        self.username = ''
        self.selected_lobby = 0
        
    def reset_lobby(self):
        self.selected_lobby = 0

user_state = __UserState()
