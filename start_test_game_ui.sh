#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <clients_number>"
    exit 1
fi

n_clients=$1
echo "Starting $n_clients client..."

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
    exit
}

trap cleanup SIGINT

wait