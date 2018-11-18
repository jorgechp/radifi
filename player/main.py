from api.api import API
from music_player.music_player import Music_player
from threading import Event, Thread




ready_event = Event()
music_player = Music_player(ready_event)
api_rest = API(music_player)
api_rest.start_api()

# music_player.play("https://www.radioalmaina.org/radio_almaina.m3u")
# ready_event.wait()


