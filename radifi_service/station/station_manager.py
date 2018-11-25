import json

from validators import url

STATION_FILE = 'config/stations'


class StationManager(object):

    def __init__(self):
        with open(STATION_FILE, 'r') as f:
            self._station_parsed_json = json.load(f)
            self._station_parsed_list = self._station_parsed_json['stations']

    def get_stations_list(self):
        return self._station_parsed_list

    def remove_station(self, id_station_to_remove):
        if id_station_to_remove < len(self._station_parsed_list):
            del self._station_parsed_list[id_station_to_remove]
            return True
        return False

    def add_station(self,name_of_station,url_of_station):
        if not self._is_name_already_exits(name_of_station) and self._is_correct_url(url_of_station):
            station_entry = {"name": name_of_station, "url" : url_of_station}
            self._station_parsed_list.append(station_entry)
            return len(self._station_parsed_list)
        else:
            return -1

    def save_stations_list(self):
        self._station_parsed_json['stations'] = self._station_parsed_list
        with open(STATION_FILE, 'w') as f:
            json.dump(self._station_parsed_json, f)

    def _is_name_already_exits(self, name):

        for station_entry in self._station_parsed_list:
            if name == station_entry['name']:
                return True
        return False

    def _is_correct_url(self, url_to_parse):
        return url(url_to_parse)