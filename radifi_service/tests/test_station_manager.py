"""
This module tests the module StationManager.
"""
import unittest

from station.station_manager import StationManager

STATION_FILE_URL = 'stations'
STATION_EMPTY_FILE_URL = 'stations_empty'


class StationManagerTest(unittest.TestCase):
    """
    This class tests the class StationManager.
    """

    def setUp(self):
        self.station_manager = StationManager(STATION_FILE_URL)

    def _get_stations_length(self):
        station_list = self.station_manager.get_stations_list()
        station_list_length = len(station_list)
        return station_list_length

    def test_get_stations_list(self):
        station_list_length = self._get_stations_length()
        self.assertGreaterEqual(station_list_length, 0)

    def test_get_five_stations_list(self):
        station_list_length = self._get_stations_length()
        self.assertEqual(station_list_length, 5)

    def test_get_zero_stations_list(self):
        station_manager_empty = StationManager(STATION_EMPTY_FILE_URL)
        station_empty_list = len(station_manager_empty.get_stations_list())
        self.assertEqual(station_empty_list, 0)

    def test_add_station(self):
        station_list_length_old = self._get_stations_length()
        self.station_manager.add_station("Test Station", "http://localhost")
        station_list_length_new = self._get_stations_length()
        self.assertEqual(station_list_length_old, station_list_length_new - 1)

    def test_remove_station(self):
        station_list_length_old = self._get_stations_length()
        id_station = self.station_manager.add_station("Test Station", "http://localhost")
        self.station_manager.remove_station(id_station)
        station_list_length_new = self._get_stations_length()
        self.assertEqual(station_list_length_old, station_list_length_new)

    def test_parse_correct_url(self):
        url_to_parse = "https://www.radioalmaina.org/radio_almaina.m3u"
        is_parsed_correctly = StationManager._is_correct_url(url_to_parse)
        self.assertTrue(is_parsed_correctly)

    def test_parse_incorrect_url(self):
        url_to_parse = "Hello World!"
        is_parsed_correctly = StationManager._is_correct_url(url_to_parse)
        self.assertFalse(is_parsed_correctly)

    def test_is_name_already_exits(self):
        duplicated_name_to_test = "Test Station"
        self.station_manager.add_station(duplicated_name_to_test, "http://localhost")
        self.station_manager.add_station(duplicated_name_to_test, "http://localhost")
        is_duplicated = self.station_manager._is_name_already_exits(duplicated_name_to_test)
        self.assertTrue(is_duplicated)

    def test_is_name_not_exits(self):
        name_to_test = "Test Station with original name"
        is_duplicated = self.station_manager._is_name_already_exits(name_to_test)
        self.assertFalse(is_duplicated)

    def test_save_stations_list(self):
        name_to_test = "New test station"
        station_list_length_first_station_manager = self._get_stations_length()
        id_new_station = self.station_manager.add_station(name_to_test, "http://localhost")
        self.station_manager.save_stations_list()
        other_station_manager = StationManager(STATION_FILE_URL)
        station_list_length_second_station_manager \
            = len(other_station_manager.get_stations_list())
        self.assertEqual(station_list_length_first_station_manager
                         , station_list_length_second_station_manager - 1)
        other_station_manager.remove_station(id_new_station)
        station_list_length_third_station_manager \
            = len(other_station_manager.get_stations_list())
        other_station_manager.save_stations_list()
        self.assertEqual(station_list_length_first_station_manager
                         , station_list_length_third_station_manager)


if __name__ == '__main__':
    unittest.main()
