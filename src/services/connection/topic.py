import enum


class Topic(enum, str):
    NEW_LOBBY = "new_lobby"
    NEW_PLAYER = "new_player"
    NEW_GAME = "new_game"
    JOIN_LOBBY = "join_lobby"
    DISCONNECT_PLAYER = "disconnect_player"
    LEAVE_LOBBY = "leave_lobby"
    DELETE_LOBBY = "delete_lobby"