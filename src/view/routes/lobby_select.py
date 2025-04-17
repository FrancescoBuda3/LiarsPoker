from nicegui import ui
from utils.state import user_state


def setup():
    from src.view.utils.layout import centered_layout
    
    @ui.page('/lobby_select')
    def lobby_select_page():
        def content():
            with ui.card():
                ui.label('Lobby Selection')
                ui.label(f'User state: {user_state}')
                lobby = ui.input(label='Lobby ID')

                def create_lobby():
                    user_state.selected_lobby = 1234
                    ui.navigate.to('/lobby')

                def join_lobby():
                    user_state.selected_lobby = lobby.value
                    ui.navigate.to('/lobby')

                ui.button('Create Lobby', on_click=create_lobby)
                ui.button('Join Lobby', on_click=join_lobby)
                ui.button('Logout', on_click=lambda: ui.navigate.to('/login'))
                
        centered_layout(content)
