from typing import Callable
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


cards_selected: list[Card] = []
card_to_box: dict[Card, ui.checkbox] = {}


def __on_checkbox_change(card, max_cards):
    if card in cards_selected:
        cards_selected.remove(card)
        card_to_box[card].value = False
    elif len(cards_selected) < max_cards:
        cards_selected.append(card)
        card_to_box[card].value = True
    else:
        card_to_box[card].value = False


def __on_submit(dialog) -> list[Card]:
    ret = cards_selected.copy()
    cards_selected.clear()
    for box in card_to_box.values():
        box.clear()
    dialog.submit(ret)


def white_cards_picker(combo: Combination,
                       max_cards: int = 5,
                       min_rank: Rank = Rank.ONE,
                       ) -> ui.dialog:
    with ui.dialog() as cards_dialog, ui.card():
        with ui.column().classes('items-center'):
            ui.label(str(combo)).classes('text-lg')
            ui.label('Select cards').classes('text-lg')
            with ui.row():
                for i in range(min_rank.value, len(Rank) + 1):
                    rank = Rank(i)
                    card = Card(None, rank)
                    with ui.column().classes('items-center'):
                        ui.image(f"static/{rank}.png",
                                 ).style('width: 5rem; height: auto')
                        checkbox = ui.checkbox(
                            value=False,
                            on_change=lambda c=card: __on_checkbox_change(
                                c, max_cards),
                        )
                        card_to_box[card] = checkbox
            ui.button(
                'Submit',
                on_click=lambda: __on_submit(cards_dialog)
            )
    return cards_dialog


def suit_picker(
        combo: Combination, 
        suits: list[Suit] = [Suit.CLUBS,Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
    ) -> ui.dialog:
    selected_suit: Suit | None = None
    suit_to_box: dict[Suit, ui.checkbox] = {}
    
    def __handle_suit_change(suit_value):
        nonlocal selected_suit
        selected_suit = Suit(suit_value)
        for suit, box in suit_to_box.items():
            box.value = suit == suit_value
            
    def __on_suit_submit(dialog) -> Suit | None:
        nonlocal selected_suit
        ret = selected_suit
        selected_suit = None
        for box in suit_to_box.values():
            box.clear()
        dialog.submit(ret)
        
    with ui.dialog() as suit_dialog, ui.card():
        with ui.column().classes('items-center'):
            ui.label(str(combo)).classes('text-lg')
            ui.label('Select suits').classes('text-lg')
            with ui.row():
                for suit in suits:
                    with ui.column().classes('items-center'):
                        ui.image(f"static/{suit}.png").style('width: 5rem; height: auto')
                        suit_to_box[suit] = ui.checkbox(
                            value=False,
                            on_change=lambda s=suit: __handle_suit_change(s)
                        )
            ui.button(
                'Submit',
                on_click=lambda: __on_suit_submit(suit_dialog)
            )
    return suit_dialog


def cards_picker(combo: Combination,
                 max_cards: int = 5,
                 suits: list[Suit] = [Suit.CLUBS,
                                     Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES],
                 min_rank: Rank = Rank.ONE
                 ) -> ui.dialog:

    with ui.dialog() as cards_dialog, ui.card():
        with ui.column().classes('items-center'):
            ui.label(str(combo)).classes('text-lg')
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
                                    c, max_cards),
                            )
                            card_to_box[card] = checkbox
            ui.button(
                'Submit',
                on_click=lambda: __on_submit(cards_dialog)
            )

    return cards_dialog


def cards_display(cards: list[Card], onClose: Callable[[], None]) -> ui.dialog:
    with ui.dialog() as display_dialog, ui.card():
        with ui.column().classes('items-center'):
            ui.label('Held cards').classes('text-lg')
            with ui.row():
                for card in cards:
                    ui.image(f"static/{card.rank}_of_{card.suit}.png"
                            ).style('width: 5rem; height: auto')
            ui.button(
                'Close',
                on_click=onClose,
            )

    return display_dialog
