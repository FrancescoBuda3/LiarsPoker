#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <clients_number>"
    exit 1
fi

if [-z "$2" && "$2" == "d"]; then
    echo "Debug mode enabled"
    debug=-"$2"
fi

n_clients=$1
pids=()

if ! pgrep -f "mosquitto.*mosquitto1.conf" > /dev/null; then
    echo "Starting primary Mosquitto (1883)..."
    if [ -z "$debug" ]; then
        mosquitto -c src/config/mosquitto1.conf -v &
    else
        mosquitto -c src/config/mosquitto1.conf &
    fi
    mosquitto1_pid=$!
    pids+=($mosquitto1_pid)
else
    echo "Primary Mosquitto already running."
fi

if ! pgrep -f "mosquitto.*mosquitto2.conf" > /dev/null; then
    echo "Starting backup Mosquitto (1884)..."
    if [ -z "$debug" ]; then
        mosquitto -c src/config/mosquitto2.conf -v &
    else
        mosquitto -c src/config/mosquitto2.conf &
    mosquitto2_pid=$!
    pids+=($mosquitto2_pid)
else
    echo "Backup Mosquitto already running."
fi

echo "Starting primary server..."
poetry run python src/controller/server/__init__.py primary $debug &
pids+=($!)

echo "Starting secondary server..."
poetry run python src/controller/server/__init__.py secondary $debug &
pids+=($!)

echo "Starting $n_clients client(s)..."
for ((i=0; i<n_clients; i++)); do
    port=$((8080 + i))
    poetry run python src/view/__init__.py $port $debug &
    pids+=($!)
    echo "Started client on port $port"
done

cleanup() {
    echo -e "\nTerminating all processes..."
    for pid in "${pids[@]}"; do
        if kill -0 $pid 2>/dev/null; then
            kill $pid
        fi
    done
    echo "All processes terminated."
    exit
}

trap cleanup SIGINT

echo "Press Ctrl+C to terminate."
wait
