"""
This is the main module of Radifi System. This module instantiate all the managers
required for managing the Radifi System as well as the APIRest, whichs is generated
by the FlaskAPI.

MANAGERS:

    * Station Manager - Manages the stations list.
    * Alarm Manager - Manager the Alarm functionality.
    * Time Manager - Deal with the Operative System Date
    * Configuration Manager - Load and handle all the Radifi settings.
"""

from threading import Event
from api.api import API
from config.config_manager import ConfigManager
from music.music_player import MusicPlayer
from station.station_manager import StationManager
from planning.time_manager import TimeManager
from planning.alarm_manager import AlarmManager

CONFIG_FILE_URL = 'config/radifi_configuration.ini'
STATION_FILE_URL = 'config/stations'

CONFIG: ConfigManager = ConfigManager(CONFIG_FILE_URL)
CONFIG.prepare_all_configs()

TIME_MANAGER = TimeManager(CONFIG)


ALARM_MANAGER = AlarmManager(CONFIG)
STATION_MANAGER = StationManager(STATION_FILE_URL)
ALARM_MANAGER.save_status()
ALARM_MANAGER.toggle_alarm(True)


READY_EVENT = Event()
MUSIC_PLAYER = MusicPlayer(READY_EVENT)
API_REST = API(MUSIC_PLAYER, STATION_MANAGER, TIME_MANAGER, ALARM_MANAGER)
API_REST.start_api()
