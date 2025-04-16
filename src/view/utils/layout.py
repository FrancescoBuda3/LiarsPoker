from nicegui import ui


def centered_layout(content_function):
    with ui.row().classes('w-full h-screen justify-center items-center'):
        with ui.column().classes('items-center'):
            content_function()
