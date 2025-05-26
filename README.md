# LiarsPoker

## How to install and run mosquitto

Mosquitto version: 1.6.9 ([Download Here](https://mosquitto.org/files/binary/win64/mosquitto-1.6.9-install-windows-x64.exe))

To run mosquitto with verbose option:

`> mosquitto -v`

## How to install dependecies and run the project

`> poetry install`

`> poetry run python [file.py]`

### Files to run

* Server: `src/controller/server/__init__.py`
* GUI: `src/view/__init__.py [port]`

### Easy Testing

Strictly for testing purposes in the same machine 
to run the server, mosquitto and the GUI you can use either scripts depending on your OS:
(**We strongly recommend to read the scripts before running them. Use at your own risk**)
* Windows: `.\start_test_game_ui.ps1 [number_of_clients]`
* Linux: `./start_test_game_ui.sh [number_of_clients]`
