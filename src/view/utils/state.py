import uuid


class __UserState:
    username: str
    selected_lobby: int
    id: uuid.UUID
    
    def __init__(self):
        self.username = ''
        self.selected_lobby = 0
        self.lobby_players = []
        self.id = uuid.uuid4()

    def __str__(self):
        return f"username={self.username}, selected_lobby={self.selected_lobby}, lobby_players={self.lobby_players}"
    
    def reset(self):
        self.username = ''
        self.selected_lobby = 0
        
    def reset_lobby(self):
        self.selected_lobby = 0
        self.lobby_players = []

user_state = __UserState()
