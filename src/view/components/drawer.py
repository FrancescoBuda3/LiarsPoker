from nicegui import ui


def hint_drawer()  -> ui.element:
    with ui.drawer('left').props('overlay bordered').style('width:25%') as drawer:
        with ui.column().style('width: 100%;'):
            with ui.row().classes('items-end justify-end'):
                ui.button(icon='close').on('click', lambda: drawer.toggle())
            ui.image(source='static/hint.JPG').style('width: 100%;')
    return drawer