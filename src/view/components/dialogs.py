from nicegui import events, ui

from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.stake.combination import Combination


def combination_picker(minimum_combo: Combination = Combination.HIGH_CARD) -> ui.dialog:
    with ui.dialog() as combination_dialog, ui.card():
        with ui.column().classes('q-pa-sm'):
            ui.label('Select Combination').classes('text-lg')
            for combo in Combination:
                bt_title = str(combo)
                bt = ui.button(
                    bt_title,
                    on_click=lambda c=combo: combination_dialog.submit(c),
                    color='primary'
                ).style('width: 100%').classes('q-mt-xs')
                if combo.value < minimum_combo.value:
                    bt.disable()

    return combination_dialog


def cards_picker(max_cards: int = 5,
                 suits: set[Suit] = {Suit.CLUBS,
                                     Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES},
                 min_rank: Rank = Rank.ONE,
                 ) -> ui.dialog:
    cards_selected: list[Card] = []
    card_to_box: dict[Card, ui.checkbox] = {}

    def __on_checkbox_change(card):
        if card in cards_selected:
            cards_selected.remove(card)
            card_to_box[card].value = False
        elif len(cards_selected) < max_cards:
            cards_selected.append(card)
            card_to_box[card].value = True
        else:
            card_to_box[card].value = False

    def __on_submit() -> list[Card]:
        ret = cards_selected.copy()
        cards_selected.clear()
        for box in card_to_box.values():
            box.clear()
        cards_dialog.submit(ret)

    with ui.dialog() as cards_dialog, ui.card():
        with ui.column().classes('items-center'):
            ui.label('Select cards').classes('text-lg')
            for suit in suits:
                with ui.row():
                    for i in range(min_rank.value, len(Rank) + 1):
                        rank = Rank(i)
                        card = Card(suit, rank)
                        with ui.column().classes('items-center'):
                            ui.image(f"static/{card.rank}_of_{card.suit}.png",
                                     ).style('width: 5rem; height: auto')
                            checkbox = ui.checkbox(
                                value=False,
                                on_change=lambda c=card: __on_checkbox_change(
                                    c),
                            )
                            card_to_box[card] = checkbox
            ui.button(
                'Submit',
                on_click=lambda: __on_submit()
            )

    return cards_dialog


def cards_display(cards: list[Card]) -> ui.dialog:
    with ui.dialog() as display_dialog, ui.card():
        for card in cards:
            ui.image(f"static/{card.rank}_of_{card.suit}.png"
                     ).style('width: 5rem; height: auto')

    return display_dialog
