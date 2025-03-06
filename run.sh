#!/bin/bash

mkdir -p "$DATAFILE_PENDING"

inotifywait -m -e create --format '%w%f' "$DATAFILE_PENDING" | while read NEW_FILE
do
    sleep 1 # Wait for file to be flushed...
    python3 main.py "$NEW_FILE"
done