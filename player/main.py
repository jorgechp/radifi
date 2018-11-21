from api.api import API
from music_player.music_player import Music_player
from threading import Event, Thread

from station_manager.station_manager import Station_manager
from time_management.Alarm_manager import Alarm_manager

alarm_manager = Alarm_manager()

station_manager = Station_manager()
ready_event = Event()
music_player = Music_player(ready_event)
api_rest = API(music_player,station_manager,alarm_manager)
api_rest.start_api()

# music_player.play("https://www.radioalmaina.org/radio_almaina.m3u")
# ready_event.wait()


