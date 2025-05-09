#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <clients_number>"
    exit 1
fi

if command -v pgrep >/dev/null; then
    pgrep mosquitto > /dev/null
    mosquitto_running=$?
else
    tasklist | grep -i mosquitto.exe > /dev/null
    mosquitto_running=$?
fi

if [ $mosquitto_running -ne 0 ]; then
    echo "Mosquitto is not running. Starting it..."
    mosquitto -v &
    mosquitto_pid=$!
else
    echo "Mosquitto is already running."
    mosquitto_pid=""
fi

n_clients=$1
echo "Starting $n_clients client(s)..."

poetry run python src/controller/server/__init__.py &
pids=($!)

for ((i=0; i<n_clients; i++)); do
    port=$((8080 + i))
    poetry run python src/view/__init__.py $port &
    pids+=($!)
done

cleanup() {
    echo "Terminating..."
    kill "${pids[@]}"
    if [ -n "$mosquitto_pid" ]; then
        kill "$mosquitto_pid"
    fi
    exit
}

trap cleanup SIGINT

wait