#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <numero_client>"
    exit 1
fi

n_clients=$1
echo n_clients

start "" "C:\Program Files\Git\git-bash.exe" -c "poetry run python src/controller/server/__init__.py"

for ((i=0; i<n_clients; i++)); do
    port=$((8080 + i))
    start "" "C:\Program Files\Git\git-bash.exe" -c "poetry run python src/view/__init__.py $port"
done