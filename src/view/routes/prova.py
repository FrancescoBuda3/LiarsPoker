from nicegui import ui

# URL di default per il dorso delle carte (devi servirlo con ui.add_static_files o CDN)
BACK_IMAGE_URL = './static/back_small.png'

def opponent_card(
    name: str,
    avatar_color: str = 'blue',      # nome colore Tailwind (es. 'red','green','blue','indigo'...)
    card_images: list[str] = None,    # lista di URL, lunghezza 1–5
    current_player: bool = False
):
    card_images = card_images or [BACK_IMAGE_URL] * 5
    # Wrapper verticale centrato
    with ui.column().classes('items-center mx-4 gap-0') as container:
        if current_player:
            ui.element('div').classes('border-solid border-t-black border-t-8 border-x-transparent border-x-8 border-b-0 mb-2')
        else:
            ui.element('div').classes('border-solid border-t-transparent border-t-8 border-x-transparent border-x-8 border-b-0 mb-2 opacity-0')
        # Avatar circolare
        ui.element('div')\
          .classes(f'bg-{avatar_color}-500 rounded-full')\
          .style('width:55px; height:55px;')
        # Nome sotto l’avatar (opzionale)
        ui.label(name).classes('mt-2 font-semibold')
        # Fila di carte
        with ui.row().classes('mt-2 gap-0'):
            for img in card_images:
                ui.image(source=img)\
                  .classes('w-12 h-18 m-1')\
                  .on('click', lambda img=img: ui.notify(f'Hai cliccato su {img}'))
    return container

def stake_card(stake_string: str):
    with ui.element('div').classes('stake-card') as container:
        ui.label(f'\"{stake_string}\"').classes('text-6xl font-bold text-gray-800')
    return stake_string


ui.add_head_html('''
  <!-- Definisci utility arbitrarie per grid-template-rows -->
  <style>
    .nicegui-content {
      height: 100vh !important;
      padding: 0 !important;
    }
    
    @layer utilities {
      .grid-rows-[5%_25%_10%_5%_13%_37%_5%] {
        grid-template-rows: 5% 25% 10% 5% 13% 37% 5%;
      }
    }
    
    @font-face {
    font-family: 'CocoSharp Trial';
    src: url('/static/fonts/Coco-Sharp-Heavy-trial') format('truetype');
    font-weight: normal;
    font-style: normal;
    }
    .stake-card {
      background-color: #e0e0e0;             /* grigio chiaro */
      border-radius: 1rem;                   /* pill shape */
      padding: 0.5rem 1.5rem;                /* verticale/orizzontale */
      display: inline-block;
      font-family: 'CocoSharp Trial', sans-serif;
      font-size: 1.25rem;                    /* circa 20px */
      font-weight: bold;
      color: #333333;
    }
    button {
        font-family: "CocoSharp Trial" !important;
        border-radius: 1rem !important; 
        color: white !important;
        padding: 1rem !important; 
        min-height: 0 !important;
    }
  </style>
''') 
with ui.element('div').classes('bg-gray-100 flex items-center justify-center basis-full h-full w-full'):
    with ui.grid(rows='5% 25% 10% 5% 13% 37% 5%') \
           .classes('w-full h-full max-w-full max-h-full grid-rows-[5%_25%_10%_5%_13%_37%_5%] border border-gray-300 gap-0 mx-[100px]'):
        with ui.row().classes('flex items-center justify-center'):
            ...
        with ui.row().classes('flex items-center justify-center'):
            opponent_card('Alice', avatar_color='red', card_images=[BACK_IMAGE_URL]*5)
            opponent_card('Alice', avatar_color='red', card_images=[BACK_IMAGE_URL]*2)
            opponent_card('Alice', avatar_color='red', card_images=[BACK_IMAGE_URL]*3)
            opponent_card('Alice', avatar_color='red', card_images=[BACK_IMAGE_URL]*5, current_player=True)
        with ui.row().classes('flex items-center justify-center'):
            stake_card('PAIR OF QUEENS')
        with ui.row().classes('flex items-center justify-center'):
            ...
        with ui.row().classes('flex items-center justify-center'):
            ui.button('RISE STAKE')\
                .classes('text-4xl font-bold')\
                .style('background-color: #00999E !important;')\
                .on('click', lambda: ui.notify('Rise Stake')) 
            ui.button('BULLSHIT')\
                .classes('text-4xl font-bold')\
                .style('background-color: #9E2500 !important;')\
                .on('click', lambda: ui.notify('Bullshit')) 
        with ui.row().classes('flex items-center justify-center'):
            card_images = ["./static/1_of_spades.png", "./static/2_of_spades.png", "./static/3_of_spades.png", "./static/4_of_spades.png", "./static/5_of_spades.png"]
            for img in card_images:
                ui.image(source=img)\
                    .style('width: 10%;')\
                    .classes('m-1')
        with ui.row().classes('flex items-center justify-center'):
            ...

    
    
ui.run()