from nicegui import ui
from utils.state import user_state
from src.services.connection.topic import Topic
from src.controller.message_factory.impl import MessageFactory
from utils.connection import connection_handler


def setup():
    from src.view.utils.layout import centered_layout

    @ui.page('/lobby_select')
    def lobby_select_page():
        message_factory = MessageFactory()

        def content():
            with ui.card():
                ui.label('Lobby Selection')
                lobby = ui.input(label='Lobby ID')

                def create_lobby():
                    ui.spinner(type='oval')
                    connection_handler.send_message(
                        message_factory.create_new_lobby_message(user_state.id), Topic.NEW_LOBBY)
                    message = connection_handler.wait_message(Topic.NEW_LOBBY)
                    while message.body["player_id"] != user_state.id:
                        message = connection_handler.wait_message(
                            Topic.NEW_LOBBY)
                    user_state.selected_lobby = message.body["lobby_id"]
                    user_state.host = True
                    ui.navigate.to('/lobby')

                def join_lobby():
                    if lobby.value == '':
                        ui.notify('Please enter a lobby ID', color='red')
                        return
                    ui.spinner(type='oval')
                    connection_handler.send_message(
                        message_factory.create_join_lobby_message(user_state.id, int(lobby.value)), Topic.JOIN_LOBBY)
                    message = connection_handler.wait_message(Topic.JOIN_LOBBY)
                    while message == None or message.body["player_id"] != user_state.id:
                        message = connection_handler.wait_message(Topic.JOIN_LOBBY)
                    if not message.body["status"]:
                        ui.notify("Error joining lobby", color='red')
                        return
                    user_state.selected_lobby = message.body["lobby_id"]
                    ui.navigate.to('/lobby')

                ui.button('Create Lobby', on_click=create_lobby)
                ui.button('Join Lobby', on_click=join_lobby)
                
                def logout():
                    connection_handler.send_message(
                        message_factory.create_remove_player_message(user_state.id), 
                        Topic.REMOVE_PLAYER
                    )
                    user_state.reset()
                    ui.navigate.to('/')
                
                ui.button('Logout', on_click=logout)

        centered_layout(content)
