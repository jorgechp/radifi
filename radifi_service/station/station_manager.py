"""
This module manages station list. The following operations are handled by this module:

    * CRUD operations over the station list

A station is defined by a name and a url. The station list is saved in a file, in json format.

Down below, a example of station list is shown:

{"stations": [
{"name": "Radio Almaina", "url": "https://www.radioalmaina.org/radio_almaina.m3u"},
{"name": "Rock FM", "url": "http://195.10.10.222/cope/rockfm.mp3"}
 ]}

"""

import json
from validators import url


class StationManager:
    """
    The class StationManager handle CRUD operations over the station list.
    """
    def __init__(self, path_to_file):
        """
        Constructor

        ARGUMENTS
            :param path_to_file The path to the station file.
            :rtype path_to_file: str
        """
        self._path_to_file = path_to_file
        self._load_stations_from_file()

    def _load_stations_from_file(self):
        """
        Load stations from file
        """
        with open(self._path_to_file, 'r') as station_file:
            self._station_parsed_json = json.load(station_file)
            self._station_parsed_list = self._station_parsed_json['stations']

    def get_stations_list(self):
        """
        Get the list of stations, parsed as a JSON dictionary.

        RETURN
            :return: The list of stations.
            :rtype: json
        """
        return self._station_parsed_list

    def remove_station(self, id_station_to_remove: int) -> bool:
        """
        Remove a station from the station list.

        ARGUMENTS
            :param id_station_to_remove: The station to remove.
            :type id_station_to_remove: int
        RETURN
            :return: True if the station was removed.
                Else if the station doesn't exists.
        """
        if id_station_to_remove < len(self._station_parsed_list):
            del self._station_parsed_list[id_station_to_remove]
            return True
        return False

    def add_station(self, name_of_station: str, url_of_station: str) -> int:
        """
        Add a new station to the station list. The name of the station must be unique.

        ARGUMENTS
            :param name_of_station: A unique name for the station.
            :type name_of_station: str
            :param url_of_station: The url of the radio station.
            :type url_of_station: str

        RETURN
            :return: The id of the new station added. Or -1 if the station name exists.
            :rtype: int
        """
        if not self._is_name_already_exits(name_of_station)\
                and self._is_correct_url(url_of_station):
            station_entry = {"name": name_of_station, "url": url_of_station}
            self._station_parsed_list.append(station_entry)
            return len(self._station_parsed_list)

        return -1

    def save_stations_list(self):
        """
        Saves the station list.
        """
        self._station_parsed_json['stations'] = self._station_parsed_list
        with open(self._path_to_file, 'w') as station_file:
            json.dump(self._station_parsed_json, station_file)

    def _is_name_already_exits(self, name: str) -> bool:
        """
        Checks if a name exists in the station list as a station name.

        ARGUMENTS

            :param name: The name of the station.
            :type name: str

        RETURN
            :return: True if the station exists, False otherwise.
            :rtype: bool
        """
        for station_entry in self._station_parsed_list:
            if name == station_entry['name']:
                return True
        return False

    @staticmethod
    def _is_correct_url(url_to_parse):
        """
        Validate the format of an url.
        Static method,

        ARGUMENTS

            :param url_to_parse: The URL to parse.
            :type url_to_parse: str

        RETURN
            :return: True if the url format is correct. False otherwise.
        """
        return url(url_to_parse)
