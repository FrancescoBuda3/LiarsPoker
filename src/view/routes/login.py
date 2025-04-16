from nicegui import ui
from utils.state import user_state


def setup():
    from src.view.utils.layout import centered_layout
    
    @ui.page('/login')
    def login_page():
        def content():
            with ui.card():
                username = ui.input(label='Username')

                def login():
                    user_state.username = username.value
                    ui.navigate.to('/lobby_select')

                ui.button('Login', on_click=login)
            
        centered_layout(content)
