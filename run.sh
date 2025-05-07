#!/bin/bash

mkdir -p "$INFLUX_WATCH_DIR"

inotifywait -m -e create --format '%w%f' "$INFLUX_WATCH_DIR" | while read NEW_FILE
do
    sleep 1 # Wait for file to be flushed...
    python3 main.py "$NEW_FILE"
done
