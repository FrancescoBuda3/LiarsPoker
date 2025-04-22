from nicegui import binding, ui
from src.model.stake.combination import Combination
from utils.state import user_state


def setup():
    from src.view.utils.layout import centered_layout
    
    __card_image_paths = ['static/four_hearts.png', 'static/four_hearts.png',
                          'static/four_hearts.png', 'static/four_hearts.png', 'static/four_hearts.png']

    @ui.page('/game')
    def game_page():
        def content():
            players = [('Alice', 'blue', 6), ('Bob', 'red', 6),
                       ('Charlie', 'green', 6), ('Diana', 'purple', 6),
                       ('Donna', 'orange', 6), ('Ernesto', 'pink', 6),
                       ('Francesco', 'brown', 6), ('Giorgio', 'cyan', 6),
                       ('Hannah', 'lime', 6)
                       ]  # Example player names and colors
            player_move = {}

            with ui.dialog() as stake_dialog, ui.card():
                with ui.column().classes('q-pa-sm'):
                    ui.label('Combinations').classes('text-lg')
                    for combo in Combination:
                        ui.button(
                            str(combo), 
                            on_click=lambda c=combo: stake_dialog.submit(str(c)), 
                            color='primary'
                        ).style('width: 100%').classes('q-mt-xs')

            async def show_stake_dialog():
                result = await stake_dialog
                ui.notify(f'You chose {result}')

            with ui.row():
                for name, color, cards in players:
                    with ui.column().classes('items-center q-mx-xl'):
                        ui.icon('circle', color=color, size='2.5rem')
                        ui.label(name).classes('text-lg')
                        rows = [min(cards, 3), max(0, cards - 3)]

                        with ui.column():
                            for num_in_row in rows:
                                if num_in_row > 0:
                                    with ui.row():
                                        for _ in range(num_in_row):
                                            ui.image('static/back.png').style('width: 0.7rem; height: auto')
                            
                        phrase = ui.label('').classes('text-lg text-gray-600').style('min-height: 1.5rem')
                        player_move[name] = phrase

            with ui.row().classes('q-gutter-md q-mt-xl'):
                ui.image('static/back.png').style('width: 100px; height: auto').classes('q-mr-xl')
                ui.image('static/blank.png').style('width: 100px; height: auto').classes('q-ml-xl')

            with ui.row().classes('q-gutter-md q-mt-xl'):
                ui.button(
                    'Bullsh*t', on_click=lambda: ui.notify("Bullsh*t!"), color='red').style('width: 10rem; height: auto')
                ui.button('Raise', on_click=lambda: show_stake_dialog(), color='green').style('width: 10rem; height: auto')

            with ui.row().classes('q-mt-xs'):
                for path in __card_image_paths:
                    ui.image(path).style('width: 120px; height: auto').classes('q-mx-sm')
                    
            with ui.row():
                ui.label(user_state.username).classes('text-lg')

            def show_player_move(player, text):
                player_move[player].set_text(f'"{text}"')

            # Example: after 2 seconds, Alice says "Bullsh*t"
            ui.timer(2.0, lambda: show_player_move(
                'Alice', 'Bullsh*t'), once=True)
        
        centered_layout(content)
