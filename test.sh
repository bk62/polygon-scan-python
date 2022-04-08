#!/usr/bin/env bash
FILE=.env
if [ -f "$FILE" ]; then
    echo "$FILE exists. Reading..."
    source .env

else 
    echo "$FILE does not exist."
fi

pytest