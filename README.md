# LiarsPoker

## How to install mosquitto

Mosquitto version: 1.6.9 ([Download Here](https://mosquitto.org/files/binary))

## How to install the python dependecies

Make sure to have Python 3.12 or higher installed ([Download Here](https://www.python.org/downloads/))

Install poetry if you don't have it already:

`pip install poetry`

Then, navigate to the project root directory and run:

`poetry install`

### How to run the project

* Mosquitto: 
    1. `mosquitto -c src/config/mosquitto1.conf [-v]`
    2. `mosquitto -c src/config/mosquitto2.conf [-v]`
* Server: 
    1. `src/controller/server/__init__.py primary [-d]`
    2. `src/controller/server/__init__.py secondary [-d]`
* GUI: 

    `src/view/__init__.py [port] [-d]`

### Easy Testing

Strictly for testing purposes in the same machine 
to run the server, mosquitto and the GUI you can use either script depending on your OS:
(**We strongly recommend reading the scripts before running them. Use at your own risk**)
* Windows: 
    
    `.\start_test_game_ui.ps1 [number_of_clients] [d]`
* Linux: 
    
    `./start_test_game_ui.sh [number_of_clients] [d]`
