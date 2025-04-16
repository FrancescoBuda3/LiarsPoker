from nicegui import ui
from utils.state import user_state


def setup():
    from src.view.utils.layout import centered_layout
    
    @ui.page('/game')
    def game_page():
        def content():
            with ui.card():
                ui.label('Game page')
                ui.label(f'User state: {user_state}')

                def back_to_lobby_select():
                    user_state.selected_lobby = None
                    ui.navigate.to('/lobby_select')

                ui.button('Back to lobby select', on_click=back_to_lobby_select)
                
        centered_layout(content)
