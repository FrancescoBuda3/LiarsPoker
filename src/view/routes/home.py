from nicegui import ui


def setup():
    from src.view.utils.layout import centered_layout
    
    @ui.page('/')
    def home():
        def content():
            ui.label('LIARS POKER!').style('font-size: 3em; font-weight: bold;')
            ui.button('Start', on_click=lambda: ui.navigate.to('/login'))
            
        centered_layout(content)
