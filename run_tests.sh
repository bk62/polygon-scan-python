#!/usr/bin/env bash
export SLOW_DOWN_API_TESTS=1
FILE=.env
if [ -f "$FILE" ]; then
    echo "$FILE exists. Reading..."
    source .env

else 
    echo "$FILE does not exist."
fi

pytest "$@"