from nicegui import ui
from src.model.player import Player
from utils.state import user_state
from src.services.connection.topic import Topic, game_topics
from src.controller.message_factory.impl import MessageFactory
from utils.connection import connection_handler, subscribe_to_game_topics, unsubscribe_from_game_topics


def setup():
    from src.view.utils.layout import centered_layout

    @ui.page('/lobby')
    def lobby_page():
        message_factory = MessageFactory()
        ready_state = False
        players: list[Player] = user_state.lobby_players

        @ui.refreshable
        def content():
            with ui.row():
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
                    
                    ui.label(f'{'Not' if not ready_state else ''} Ready')
                    
                    def switch_ready():
                        nonlocal ready_state
                        ready_state = not ready_state
                        connection_handler.send_message(
                            message_factory.create_ready_to_play_message(
                                user_state.id, user_state.selected_lobby, ready_state),
                            Topic.READY_TO_PLAY)
                        content.refresh()

                    ui.button('Set Not Ready' if ready_state else 'Set Ready', on_click=switch_ready)

                    def back_to_lobby_select():
                        unsubscribe_from_game_topics(user_state.selected_lobby)
                        connection_handler.send_message(
                            MessageFactory().create_leave_lobby_message(
                                user_state.id, user_state.selected_lobby),
                            Topic.LEAVE_LOBBY
                        )
                        user_state.reset_lobby()
                        ui.navigate.to('/lobby_select')

                    ui.button('Back to lobby selection', on_click=back_to_lobby_select)
                
                def check_for_players():
                    nonlocal players
                    message = connection_handler.no_wait_message(Topic.JOIN_LOBBY)
                    if message and message.body["lobby_id"] == user_state.selected_lobby:
                        user_state.lobby_players = message.body["players_in_lobby"]
                        players = message.body["players_in_lobby"]
                        content.refresh()
                    
                    message = connection_handler.no_wait_message(Topic.READY_TO_PLAY)
                    if message and message.body["lobby_id"] == user_state.selected_lobby:
                        for player in players:
                            if player.id == message.body["player_id"]:
                                player.ready = message.body["ready"]
                        content.refresh()
                        
                ui.timer(1, check_for_players)
            
                        
                with ui.card():
                    ui.label(f'Players Ready:')
                    for player in players:
                        ui.label(f'{player.username} {"✅" if player.ready else "❌"}')
                        
        subscribe_to_game_topics(user_state.selected_lobby)
        centered_layout(content)

        def wait_start_game():
            message = connection_handler.no_wait_message(Topic.START_GAME)
            if message and message.body["lobby_id"] == user_state.selected_lobby:
                ui.navigate.to('/game')
                return False
        
        ui.timer(0.5, wait_start_game)
