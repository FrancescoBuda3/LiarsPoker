from nicegui import ui
from utils.state import user_state


def setup():
    from src.view.utils.layout import centered_layout
    
    @ui.page('/lobby')
    def lobby_page():
        def content():
            with ui.card():
                ui.label('Lobby page')
                ui.label(f'User state: {user_state}')
                ui.button('Start Game', on_click=lambda: ui.navigate.to('/game'))

                def back_to_lobby_select():
                    user_state.selected_lobby = None
                    ui.navigate.to('/lobby_select')

                ui.button('Back to lobby selection', on_click=back_to_lobby_select)
            
        centered_layout(content)
