
from api.api import API
from config.Config_manager import Config_manager
from music.music_player import MusicPlayer
from threading import Event

from station.station_manager import StationManager
from time.Alarm_manager import AlarmManager
from time.Time_manager import TimeManager

CONFIG_FILE_URL = 'config/radifi_configuration.ini'

config = Config_manager(CONFIG_FILE_URL)
config.prepare_all_configs()
general_config = config.get_properties_group('GENERAL')

time_manager = TimeManager(config)


alarm_manager = AlarmManager(config)
station_manager = StationManager()
alarm_manager.save_status()
alarm_manager.toggle_alarm(True)


ready_event = Event()
music_player = MusicPlayer(ready_event)
api_rest = API(music_player,station_manager,time_manager,alarm_manager)
api_rest.start_api()

