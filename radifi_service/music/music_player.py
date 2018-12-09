"""
This module manages the audio player, sending to the VLC library the sound
stream to be played by the System.
"""

import os
import time
import requests
import vlc
import alsaaudio


class MusicPlayer:
    """
    The class MusicPlayer represent the player, which performs the following operations:

    * Start/Stop the player.
    * Check if the player is busy.
    * Get information about the current stream.
    """

    def __init__(self, config, ready_event=None):
        """
        Constructor.

        ARGUMENTS
            :param config: A ConfigManager instance.
            :type config: ConfigManager
            :param ready_event: Optional parameter,
                if set, it can be use as a signal to help concurrent threads to
            be synchronized.
            :type ready_event: Event
        """
        self._config = config
        self._vlc_instance = vlc.Instance()
        self._ready = ready_event
        self._url = None
        self._player = None
        self._is_played_succesfully = False
        self._error_code = 0
        self._alsa_audio = alsaaudio.Mixer()

    def is_played_successfully(self):
        """
        Checks if the stream was played successfully.

        RETURM
            :return: True if the stream was played properly. False otherwise.
            :rtype: bool
        """
        return self._is_played_succesfully

    def is_playing(self):
        """
        Checks if the player is currently busy.

        RETURM
            :return: True if the player is busy. False otherwise.
            :rtype: bool
        """
        return self._player is not None

    def play(self, url):
        """
        Tell the player to play the current streaming url.

        ARGUMENT
            :param url: The streaming url.
            :type url: string
        RETURN
            :return: True if the straming is being played. False otherwise.
            :rtype: bool
        """
        self._url = url
        self._play_sound()

    def _play_sound(self):
        """
        Play the url specified. It can be a remote url or a local file.
        RETURN
            :return: True if the straming is being played. False otherwise.
            :rtype: bool
        """

        if self.is_playing():
            self._is_played_succesfully = False
            return

        is_local_file = self._url[:4] == 'file'
        if is_local_file:
            is_found = os.path.isfile(self._url[7:])
        else:
            remote_request = requests.get(self._url, stream=True)
            is_found = remote_request.ok

        if is_found:
            media_list = self._vlc_instance.media_list_new([self._url])
            if is_local_file:
                self._player = self._vlc_instance.media_player_new()
                media_to_set = self._vlc_instance.media_new(self._url)
                self._player.set_media(media_to_set)
            else:
                self._player = self._vlc_instance.media_list_player_new()
                self._player.set_media_list(media_list)

            self._player.play()
            time.sleep(0.5)
            self._is_played_succesfully = True
        else:
            self._error_code = 2
            self._is_played_succesfully = False

    def play_alarm(self, is_default_song=0):
        """
        Plays the alarm.

        ARGUMENTS
            :param is_default_song: True if the alarm should be
                triggered using the default alarm song.
            :type is_default_song: bool
        RETURN
            :return: True if the straming is being played. False otherwise.
            :rtype: bool
        """
        alarm_configuration = self._config['ALARM']
        url_to_play = alarm_configuration['default_station_url']
        if is_default_song or url_to_play:
            abs_path = os.path.abspath(alarm_configuration['default_alarm_path'])
            url_to_play = "file://" + abs_path
        self.play(url_to_play)

    def stop_player(self):
        """
        Stops the player.
        """
        if self._player is not None:
            self._player.stop()
            self._ready.set()
            self._player = None
            return True

        return False

    def get_current_station_url(self):
        """
        Get the current station url being played.

        RETURN
            :return: The url of the station
            :rtype: string
        """
        return self._url

    def get_current_volume(self):
        """
        Get the current volume.

        RETURN
            :return: The url of the station
            :rtype: string
        """
        if self.is_playing():
            return self._alsa_audio.getvolume()
        else:
            return -1

    def set_current_volume(self, volume_to_set):
        """
        Changes the current volume.

        ARGUMENTS
            :param volume_to_set: value between 0 and 100
            :type volume_to_set: int
        """

        volume_to_set = min(volume_to_set,100)
        volume_to_set = max(volume_to_set,0)

        self._alsa_audio.setvolume(volume_to_set)