import json

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
        station_entry = {"name": name_of_station, "url" : url_of_station}
        self.__station_parsed_list.append(station_entry)

    def save_stations_list(self):
        self.__station_parsed_json['stations'] = self.__station_parsed_list
        with open(STATION_FILE, 'w') as f:
            json.dump(self.__station_parsed_json, f)