from nicegui import ui
from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.player import Player
from src.model.stake import Stake
from src.model.stake.combination import Combination
from utils.state import user_state


def setup():
    from src.view.utils.layout import centered_layout
    from src.view.components.dialogs import cards_picker, combination_picker
    
    __player_colors = [
        'red', 'blue', 'green', 'yellow',
        'purple', 'orange', 'pink', 'brown',
        'cyan', 'lime'
    ]

    @ui.page('/game')
    def game_page():
        def content():
            players: list[Player] = [
                Player("Alice", 0), Player("Bob", 0),
                Player("Charlie", 0), Player("Dave", 0),
                Player("Eve", 0), Player("Frank", 0),
                Player("Grace", 0), Player("Heidi", 0),
                Player("Ivan", 0),
            ]
            for player in players:
                player.cards_in_hand = 6
                
            cards_in_hand: list[Card] = [
                Card(Suit.SPADES, Rank.JACK),
                Card(Suit.HEARTS, Rank.QUEEN),
                Card(Suit.DIAMONDS, Rank.KING),
                Card(Suit.CLUBS, Rank.ACE),
            ]

            async def show_stake_dialog(min_stake: Stake):
                combo = await combination_picker(min_stake.combo)
                max_cards = 5
                match combo:
                    case (
                        Combination.HIGH_CARD
                        | Combination.PAIR
                        | Combination.THREE_OF_A_KIND
                        | Combination.FOUR_OF_A_KIND
                    ):
                        max_cards = 1
                    case (
                        Combination.TWO_PAIR
                        | Combination.FULL_HOUSE
                    ):
                        max_cards = 2                       
                cards = await cards_picker(max_cards=max_cards)
                if check_input(cards, combo):
                    ui.notify(f'You chose {combo} with cards {cards}')
                else:
                    ui.notify('Invalid input!')
                    
            def check_input(cards: list[Card], combo: Combination) -> bool:
                if combo == Combination.STRAIGHT:
                    cards.sort(key=lambda x: x.rank.value)
                    return all(
                        cards[i].rank.value == cards[i + 1].rank.value - 1
                        for i in range(len(cards) - 1)
                    )
                elif combo == Combination.FLUSH:
                    return all(
                        cards[i].suit == cards[i + 1].suit
                        for i in range(len(cards) - 1)
                    )
                elif combo == Combination.STRAIGHT_FLUSH:
                    cards.sort(key=lambda x: x.rank.value)
                    return all(
                        cards[i].suit == cards[i + 1].suit
                        for i in range(len(cards) - 1)
                    ) and all(
                        cards[i].rank.value == cards[i + 1].rank.value - 1
                        for i in range(len(cards) - 1)
                    )
                elif combo == Combination.ROYAL_FLUSH:
                    cards.sort(key=lambda x: x.rank.value)
                    return all(
                        cards[i].suit == cards[i + 1].suit
                        for i in range(len(cards) - 1)
                    ) and all(
                        cards[i].rank.value == Rank(i + 10).value
                        for i in range(len(cards))
                    )
                elif combo == Combination.HIGH_CARD or combo == Combination.PAIR or combo == Combination.THREE_OF_A_KIND or combo == Combination.FOUR_OF_A_KIND or combo == Combination.TWO_PAIR or combo == Combination.FULL_HOUSE:
                    return True
                    
                
                
            players_moves = {}
                
            def show_player_move(player, text):
                players_moves[player].set_text(f'"{text}"')

            with ui.row().classes('justify-center'):
                for i in range(len(players)):
                    player: Player = players[i]
                    with ui.column().classes('col-2 items-center'):
                        ui.icon('circle', color=__player_colors[i], size='1.5rem')
                        ui.label(player.username).classes('text-lg')
                        with ui.row():
                            for _ in range(player.cards_in_hand):
                                ui.image('static/back.png'
                                    ).style('width: 0.7rem; height: auto')
                        move = ui.label(''
                            ).classes('text-lg text-gray-600'
                            ).style('min-height: 1.5rem')
                        players_moves[player.username] = move

            ui.image('static/back.png'
                ).style('width: 6rem; height: auto'
                ).classes('q-mr-xl')

            with ui.row():
                ui.button(
                    'Bullsh*t', 
                    on_click=lambda: ui.notify("Bullsh*t!"), 
                    color='red'
                    ).style('width: 10rem; height: auto')
                ui.button(
                    'Raise', 
                    on_click=lambda: show_stake_dialog(Stake(Combination.HIGH_CARD, 1)),
                    color='green'
                    ).style('width: 10rem; height: auto')

            with ui.row():
                for card in cards_in_hand:
                    ui.image(f"static/{card.rank}_of_{card.suit}.png"
                        ).style('width: 6.5rem; height: auto'
                        ).classes('q-mx-sm')

            with ui.row():
                ui.label(user_state.username).classes('text-lg')

            # Example: after 2 seconds, Alice says "Bullsh*t"
            ui.timer(2.0, lambda: show_player_move(
                'Alice', 'Bullsh*t'), once=True)

        centered_layout(content)
