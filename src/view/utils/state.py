import uuid


class __UserState:
    def __init__(self):
        self.username = None
        self.selected_lobby = None
        self.id = uuid.uuid4()
        self.host = False

    def __str__(self):
        return f"username={self.username}, selected_lobby={self.selected_lobby}"
    
    def reset(self):
        self.username = None
        self.selected_lobby = None
        self.host = False

user_state = __UserState()
