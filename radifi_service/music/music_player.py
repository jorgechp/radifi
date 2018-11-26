import configparser
import requests
import vlc
import os
import planning

from threading import Event, Thread

CONFIG_FILE_URL = 'config/radifi_configuration.ini'

class MusicPlayer(object):

    def __init__(self,ready_event = None):
        """
        Default constructor
        """
        self._config = configparser.ConfigParser()
        self._config.read(CONFIG_FILE_URL)
        self._vlc_instance = vlc.Instance()
        self._ready = ready_event
        self._url = None
        self._player = None
        self._is_played_succesfully = False

    def is_played_successfully(self):
        return self._is_played_succesfully

    def is_playing(self):
        return self._player != None

    def play(self,url):
        self._url = url
        self._play_sound()

    def _play_sound(self):
        """
        Play the url specified. It can be a remote url or a local file.
        """

        if self.is_playing():
            self._is_played_succesfully = False
            return

        is_local_file = self._url[:4] == 'file'
        if (is_local_file):
            is_found = os.path.isfile(self._url[7:])
        else:
            remote_request = requests.get(self._url, stream=True)
            is_found = remote_request.ok

        if(is_found):
            media_list = self._vlc_instance.media_list_new([self._url])
            if(is_local_file):
                self._player = self._vlc_instance.media_player_new()
                media_to_set = self._vlc_instance.media_new(self._url)
                self._player.set_media(media_to_set)
            else:
                self._player = self._vlc_instance.media_list_player_new()
                self._player.set_media_list(media_list)

            self._player.play()
            planning.sleep(0.5)
            self._is_played_succesfully = True
        else:
            self._error_code = 2
            self._is_played_succesfully = False


    def play_alarm(self, is_default_song = 0):
        alarm_configuration = self._config['ALARM']
        url_to_play = alarm_configuration['default_station_url']
        if(is_default_song or len(url_to_play) == 0):
            abs_path = os.path.abspath(alarm_configuration['default_alarm_path'])
            url_to_play = "file://" + abs_path
        self.play(url_to_play)


    def stop_player(self):
        self._player.stop()
        self._player = None

    def stop_sound(self):
        if(self._player != None):
            self._player.stop()
            self._ready.set()
            self._player = None
            return True
        else:
            return False


    def get_thread(self):
        return self.__thread

    def get_current_station_url(self):
        return self._url
