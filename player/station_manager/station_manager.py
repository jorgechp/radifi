import json

from validators import url

STATION_FILE = 'config/stations'


class Station_manager(object):

    def __init__(self):
        with open(STATION_FILE, 'r') as f:
            self.__station_parsed_json = json.load(f)
            self.__station_parsed_list = self.__station_parsed_json['stations']

    def get_stations_list(self):
        return self.__station_parsed_list

    def remove_station(self, id_station_to_remove):
        if id_station_to_remove < len(self.__station_parsed_list):
            del self.__station_parsed_list[id_station_to_remove]
            return True
        return False

    def add_station(self,name_of_station,url_of_station):
        if not self.__is_name_already_exits(name_of_station) and self.__is_correct_url(url_of_station):
            station_entry = {"name": name_of_station, "url" : url_of_station}
            self.__station_parsed_list.append(station_entry)
            return len(self.__station_parsed_list)
        else:
            return -1

    def save_stations_list(self):
        self.__station_parsed_json['stations'] = self.__station_parsed_list
        with open(STATION_FILE, 'w') as f:
            json.dump(self.__station_parsed_json, f)

    def __is_name_already_exits(self, name):

        for station_entry in self.__station_parsed_list:
            if name == station_entry['name']:
                return True
        return False

    def __is_correct_url(self, url_to_parse):
        return url(url_to_parse)