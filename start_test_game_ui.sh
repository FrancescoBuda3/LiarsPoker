#!/bin/bash

clients_number=$1
debuggable=$2

if [[ -z "$clients_number" ]]; then
    echo "Usage: ./start_clients.sh <clients_number> <debug>"
    exit 1
fi

if [[ "$debuggable" == "d" ]]; then
    echo "Debug mode enabled"
    debuggable="-d"
else
    debuggable=""
fi

is_mosquitto_running() {
    ps aux | grep "mosquitto" | grep "$1" | grep -v "grep" > /dev/null
}

kill_mosquitto_by_conf() {
    ps | grep "mosquitto" | grep "$1" | grep -v "grep" | awk '{print $1}' | xargs -r kill
}

if ! is_mosquitto_running "mosquitto1.conf"; then
    echo "Starting primary Mosquitto (1883)..."
    if [[ "$debuggable" == "-d" ]]; then
        mosquitto -c src/config/mosquitto1.conf -v &
    else
        mosquitto -c src/config/mosquitto1.conf &
    fi
else
    echo "Primary Mosquitto already running."
fi

if ! is_mosquitto_running "mosquitto2.conf"; then
    echo "Starting backup Mosquitto (1884)..."
    if [[ "$debuggable" == "-d" ]]; then
        mosquitto -c src/config/mosquitto2.conf -v &
    else
        mosquitto -c src/config/mosquitto2.conf &
    fi
else
    echo "Backup Mosquitto already running."
fi

echo "Starting $clients_number client(s)..."

poetry run python src/controller/server/__init__.py primary $debuggable &
server1_pid=$!

poetry run python src/controller/server/__init__.py secondary $debuggable &
server2_pid=$!

client_pids=()

for ((i=0; i<clients_number; i++)); do
    port=$((8080 + i))
    poetry run python src/view/__init__.py "$port" $debuggable &
    client_pids+=($!)
    echo "Started client on port $port"
done

kill_if_running() {
    if ps -p "$1" > /dev/null 2>&1; then
        kill "$1"
    fi
}

cleanup() {
    echo -e "\nTerminating processes..."

    kill_mosquitto_by_conf "mosquitto1.conf"
    kill_mosquitto_by_conf "mosquitto2.conf"

    kill_if_running $server1_pid
    kill_if_running $server2_pid

    for pid in "${client_pids[@]}"; do
        kill_if_running $pid
    done

    echo "All processes terminated."
    exit
}

trap cleanup SIGINT SIGTERM

echo "Press Ctrl+C to terminate."
while true; do
    sleep 1
done
