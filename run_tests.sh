#!/usr/bin/env bash
export SLEEP_BETWEEN_TESTS=2
# force record
export BETAMAX_RECORD_MODE=all
FILE=.env
if [ -f "$FILE" ]; then
    echo "$FILE exists. Reading..."
    source .env

else 
    echo "$FILE does not exist."
fi

poetry run pytest "$@"

# reset
export BETAMAX_RECORD_MODE=0