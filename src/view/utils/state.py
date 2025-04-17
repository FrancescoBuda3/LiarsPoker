import uuid


class __UserState:
    def __init__(self):
        self.username = None
        self.selected_lobby = None
        self.id = uuid.uuid4()

    def __str__(self):
        return f"username={self.username}, selected_lobby={self.selected_lobby}"


user_state = __UserState()
