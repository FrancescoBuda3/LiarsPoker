from nicegui import ui

from src.model.stake import Stake

def opponent_component(
    name: str,
    avatar_color: str,
    cards: int,
    current_player: bool
):
    card_images = ['./static/back_small.png'] * cards
    current_player_class = 'border-t-black' if current_player else 'border-t-transparent opacity-0'
    with ui.column().classes('items-center mx-4 gap-0') as opponent_container:
        ui.element('div')\
            .classes(
                f'border-solid border-t-8 border-x-transparent border-x-8 border-b-0 mb-2 {current_player_class}')
        ui.element('div')\
          .classes(f'bg-{avatar_color}-500 rounded-full')\
          .style('width:55px; height:55px;')
        ui.label(name).classes('mt-2 font-semibold')
        with ui.row().classes('mt-2 gap-0'):
            for img in card_images:
                ui.image(source=img)\
                  .classes('w-12 h-18 m-1')
    return opponent_container


def stake_display(stake: Stake | None):
    if stake:
        move: str = f"{stake.combo}: "
        for i, r in enumerate(stake.ranks):
            if i != 0:
                move += ", "
            move += f"{r.to_symbol()}"
        if stake.suits:
            move += " of "
        for i, s in enumerate(stake.suits):
            if i != 0:
                move += " and "
            move += f"{s}"
        with ui.element('div').classes('stake-card') as stake_container:
                ui.label(move)\
                    .classes('text-4xl font-bold text-gray-800')
        return stake_container