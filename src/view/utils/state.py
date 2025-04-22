import os
import uuid


class __UserState:
    def __init__(self, sessionId=None):
        self.sessionId = None
        self.username = None
        self.selected_lobby = None
        self.id = uuid.uuid4()

    def __str__(self):
        return f"username={self.username}, selected_lobby={self.selected_lobby}"

client_id = os.getenv('CLIENT_ID', 'FixedName')
user_state = __UserState(sessionId=client_id)
