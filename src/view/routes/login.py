from nicegui import ui
from src.controller.message_factory.impl import MessageFactory
from src.services.connection.topic import Topic
from utils.state import user_state
from utils.connection import connection_handler

def setup():
    from src.view.utils.layout import centered_layout

    @ui.page('/login')
    def login_page():
        message_factory = MessageFactory()

        def content():
            with ui.card():
                username = ui.input(label='Username')

                def login():
                    connection_handler.send_message(message_factory.create_new_player_message(
                        username.value, user_state.id), Topic.NEW_PLAYER)
                    user_state.username = username.value
                    ui.navigate.to('/lobby_select')

                ui.button('Login', on_click=login)

        centered_layout(content)
