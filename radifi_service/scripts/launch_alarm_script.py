import sys
import requests
from time import sleep

TRIALS_LIMIT = 10

def execute(url,port):

    path = "/alarm/play"
    param_not_default_song = "defaultSong=0"
    param_default_song = "defaultSong=1"

    url_parsed = url + ":" + str(port) + path + "?"
    url_to_call = url_parsed + param_not_default_song

    response = requests.get(url_to_call)

    url_to_call = url_parsed + param_default_song
    num_of_trials = 0
    while(response.status_code != 200 and num_of_trials < TRIALS_LIMIT):
        sleep(5)
        response = requests.get(url_to_call)
        num_of_trials = num_of_trials + 1

    if num_of_trials == TRIALS_LIMIT:
        print("FATAL ERROR: THE NUMBER OF REQUESTS EXECUTED EXCEDEED THE LIMIT WITHOUT SUCCESS. THE ALARM HAS NOT BEEN TRIGGERED!!!", file=sys.stderr)
        sys.exit(2)
    print("THE ALARM HAS BEEN TRIGGERED, HAVE A GOOD DAY")
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        error_message = """Usage: ./launch_alarm_script.py <url> <port>"""
        print(error_message, file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    url = url[:-1] if url[-1] == '/' else url  # Remove last / from the url
    port = sys.argv[2]
    execute(url,port)