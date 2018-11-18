import requests
import vlc
import os
import time

from threading import Event, Thread


class Music_player(object):

    def __init__(self,ready_event = None):
        """
        Default constructor
        """
        self.__vlc_instance = vlc.Instance()
        self.__ready = ready_event
        self.__url = None

    def play(self,url):

        self.__url = url
        self.__thread = Thread(target=self.__play_sound)
        self.__thread.start()



    def __play_sound(self):
        """
        Play the url specified. It can be a remote url or a local file.
        :param url: The url with the file to be played.
        :return: True if the sound could be played, False otherwise.
        """

        is_played_succesfully = True
        is_local_file = self.__url[:4] == 'file'
        if (is_local_file):
            is_found = os.path.isfile(self.__url[7:])
        else:
            remote_request = requests.get(self.__url, stream=True)
            is_found = remote_request.ok

        if(is_found):
            media_list = self.__vlc_instance.media_list_new([self.__url])
            if(is_local_file):
                self.__player = self.__vlc_instance.media_player_new()
                media_to_set = self.__vlc_instance.media_new(url)
                media_list.get_mrl()
                self.__player.set_media(media_to_set)
            else:
                self.__player = self.__vlc_instance.media_list_player_new()
                self.__player.set_media_list(media_list)

            self.__player.play()
            time.sleep(0.5)
        else:
            self._error_code = 2
            is_played_succesfully = False

        return is_played_succesfully

    def stop_sound(self):
        self.__player.stop()
        self.__ready.set()

    def get_thread(self):
        return self.__thread

    def get_current_station_url(self):
        return self.__url
