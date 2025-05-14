from nicegui import ui
from utils.state import user_state
from src.services.connection.topic import Topic, game_topics
from src.controller.message_factory.impl import MessageFactory
from utils.connection import connection_handler


def setup():
    from src.view.utils.layout import centered_layout

    @ui.page('/lobby')
    def lobby_page():

        def __subscribe_to_game_topics():
            for topic in game_topics:
                connection_handler.subscribe(
                    "lobby/" + str(user_state.selected_lobby) + topic)

        def content():
            with ui.card():
                ui.label('Lobby page')
                ui.label('Lobby ID:')

                def copy_lobby_id():
                    ui.clipboard.write(f'{user_state.selected_lobby}')
                    ui.notify('Lobby ID copied to clipboard')

                ui.button(
                    f'{user_state.selected_lobby} 📋',
                    color="secondary",
                    on_click=lambda: copy_lobby_id()
                )

                if user_state.host:
                    ui.button('Start Game', on_click=lambda: start_game())

                def start_game():
                    connection_handler.send_message(
                        MessageFactory().create_new_game_message(
                            user_state.selected_lobby), Topic.NEW_GAME
                    )
                    __subscribe_to_game_topics()
                    ui.navigate.to('/game')

                def back_to_lobby_select():
                    connection_handler.send_message(
                        MessageFactory().create_leave_lobby_message(user_state.selected_lobby),
                        Topic.LEAVE_LOBBY
                    )
                    user_state.selected_lobby = None
                    user_state.host = False
                    ui.navigate.to('/lobby_select')

                ui.button('Back to lobby selection',
                          on_click=back_to_lobby_select)

        centered_layout(content)

        if not user_state.host:
            def check_for_new_game():
                message = connection_handler.no_wait_message(Topic.NEW_GAME)
                if message and message.body["lobby_id"] == user_state.selected_lobby:
                    __subscribe_to_game_topics()
                    ui.navigate.to('/game')
                    return False

            ui.timer(0.5, check_for_new_game)
