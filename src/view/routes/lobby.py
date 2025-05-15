from nicegui import ui
from utils.state import user_state
from src.services.connection.topic import Topic, game_topics
from src.controller.message_factory.impl import MessageFactory
from utils.connection import connection_handler


def setup():
    from src.view.utils.layout import centered_layout
    
    @ui.page('/lobby')
    def lobby_page():
        for topic in game_topics:
            connection_handler.subscribe(
                "lobby/" + str(user_state.selected_lobby) + topic) 
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
                    
                    if user_state.host:
                        ui.button('Start Game', on_click=lambda: start_game())
                    
                    def start_game():
                        if len(user_state.players_in_lobby) < 2:
                            ui.notify('Not enough players to start the game', color='red')
                            return
                        connection_handler.send_message(
                            MessageFactory().create_new_game_message(user_state.selected_lobby), Topic.NEW_GAME
                        )
                        ui.navigate.to('/game')

                    def back_to_lobby_select():
                        user_state.selected_lobby = None
                        ui.navigate.to('/lobby_select')

                    ui.button('Back to lobby selection', on_click=back_to_lobby_select)
                with ui.card():
                    ui.label('Players:')
                    if user_state.host and user_state.players_in_lobby == []:
                        ui.label(user_state.username)
                    for player in user_state.players_in_lobby:
                        ui.label(player.username)
                
                def check_for_new_player():
                    message = connection_handler.no_wait_message(Topic.JOIN_LOBBY)
                    if message and message.body["lobby_id"] == user_state.selected_lobby:
                        # print(message.body["players_in_lobby"])
                        user_state.players_in_lobby = message.body["players_in_lobby"]
                        content.refresh()
                        ui.notify('New player joined')
                        # content.refresh()
                ui.timer(1, check_for_new_player)
                # Poll every second
                        
                                
        centered_layout(content)
        if not user_state.host:
            def check_for_new_game():
                message = connection_handler.no_wait_message(Topic.NEW_GAME)
                if message and message.body["lobby_id"] == user_state.selected_lobby:
                    ui.navigate.to('/game')
                    return False  # stop the timer

            # Poll every 0.5 seconds
            ui.timer(0.5, check_for_new_game)
        
                
