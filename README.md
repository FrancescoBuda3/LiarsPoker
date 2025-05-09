# LiarsPoker

## How to install and run mosquitto

Mosquitto version: 1.6.9 link: [Download](https://mosquitto.org/files/binary/win64/mosquitto-1.6.9-install-windows-x64.exe)

mosquitto -v to run mosquitto with verbose option

## How to install dependecies and run the project

`> poetry install`

`> poetry run python [file.py]`

to update the poetry configuration run:

`> poetry lock --no-update`

`> poetry install`

## Files to run

* Server: `src/controller/server/__init__.py`
* GUI: `src/view/__init__.py [port]`
