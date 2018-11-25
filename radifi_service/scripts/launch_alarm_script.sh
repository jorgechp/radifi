#!/bin/bash

TRIALS_LIMIT=10
DESIRED_SLEEP_SECONDS=5

if [ "$#" -ne 2 ]; then
    echo "Usage: ./launch_alarm_script.py <url> <port>"
    exit 1
fi

URL=${1}
PORT=${2}
PATH="alarm/play"
PARAM_NOT_DEFAULT_SONG="defaultSong=0"
PARAM_DEFAULT_SONG="defaultSong=1"

URL_PARSED="$URL:$PORT/$PATH?"
URL_TO_CALL="$URL_PARSED$PARAM_NOT_DEFAULT_SONG"

response=`/usr/bin/curl --silent --write-out "%{http_code}\n" "$URL_TO_CALL"`

URL_TO_CALL="$URL_PARSED$PARAM_DEFAULT_SONG"

trial_counter=0
while [ "$response" -ne 204 ] && [ "$trial_counter" -lt "$TRIALS_LIMIT" ]; do
    /bin/sleep "$DESIRED_SLEEP_SECONDS"s
    response=`/usr/bin/curl --silent --write-out "%{http_code}\n" "$URL_TO_CALL"`
    trial_counter=$((trial_counter + 1))
    echo $trial_counter
done

if [ "$trial_counter" -eq "$TRIALS_LIMIT" ]; then
    echo "FATAL ERROR: THE NUMBER OF REQUESTS EXECUTED EXCEDEED THE LIMIT WITHOUT SUCCESS. THE ALARM HAS NOT BEEN TRIGGERED!!!"
    exit 2
fi

echo "THE ALARM HAS BEEN TRIGGERED, HAVE A GOOD DAY"
exit 0


