
from api.api import API
from config.Config_manager import Config_manager
from music_player.music_player import Music_player
from threading import Event

from station_manager.station_manager import Station_manager
from time_management.Alarm_manager import Alarm_manager
from time_management.Time_manager import Time_manager

CONFIG_FILE_URL = 'config/radifi_configuration.ini'

config = Config_manager(CONFIG_FILE_URL)
config.prepare_all_configs()
general_config = config.get_properties_group('GENERAL')

time_manager = Time_manager(config)


alarm_manager = Alarm_manager(config)
station_manager = Station_manager()
alarm_manager.save_status()
alarm_manager.toggle_alarm(True)


ready_event = Event()
music_player = Music_player(ready_event)
api_rest = API(music_player,station_manager,time_manager,alarm_manager)
api_rest.start_api()

