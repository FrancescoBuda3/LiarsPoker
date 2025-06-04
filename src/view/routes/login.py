from nicegui import ui
from src.controller.message_factory.impl import MessageFactory
from src.services.connection.topic import Topic
from utils.state import user_state
from utils.connection import connection_handler

def setup(debug: bool = False):
    from src.view.utils.layout import centered_layout
    if debug:
        connection_handler.set_debug(True)

    @ui.page('/login')
    def login_page():
        message_factory = MessageFactory()

        def content():
            with ui.card():
                username = ui.input(label='Username')

                def login():
                    if username.value == '':
                        ui.notify("Please enter a username", color='red')
                        return
                    ui.spinner(type='oval')
                    connection_handler.send_message(
                        message_factory.create_new_player_message(
                            username.value, user_state.id), 
                        Topic.NEW_PLAYER)
                    response = connection_handler.wait_message(Topic.NEW_PLAYER)
                    while response == None or response.body["player_id"] != user_state.id:
                        response = connection_handler.wait_message(Topic.NEW_PLAYER)
                    if response.body["response"]:
                        user_state.username = username.value
                        ui.navigate.to('/lobby_select')
                    else:
                        ui.notify("Error joining lobby", color='red')

                ui.button('Login', on_click=login)

        centered_layout(content)
