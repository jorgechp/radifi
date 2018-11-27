"""
This module tests the module Alarm Manager.
"""
import unittest

from alarm_manager import AlarmManager
from config_manager import ConfigManager

CONFIG_FILE_URL = 'radifi_test_configuration.ini'
class AlarmManagerTest(unittest.TestCase):

    def setUp(self):
        config = ConfigManager(CONFIG_FILE_URL)
        self.alarm_manager = AlarmManager(config)

    def test_get_current_alarm_is_tuple(self):
        date = self.alarm_manager.get_current_alarm()
        self.assertIsInstance(date,tuple)

    def test_get_current_alarm(self):
        hour,minute = self.alarm_manager.get_current_alarm()
        self.assertTrue(hour.isdigit())
        self.assertTrue(minute.isdigit())
        self.assertGreaterEqual(int(hour),0)
        self.assertGreaterEqual(int(minute),0)
        self.assertLessEqual(int(hour),24)
        self.assertLessEqual(int(hour),60)

    def test_is_alarm_enabled(self):
        is_alarm_enabled = self.alarm_manager.is_alarm_enabled()
        self.assertIsInstance(is_alarm_enabled,bool)

    def test_toggle_alarm(self):
        self.alarm_manager.toggle_alarm(True)
        is_alarm_enabled = self.alarm_manager.is_alarm_enabled()
        self.assertTrue(is_alarm_enabled)
        self.alarm_manager.toggle_alarm(False)
        is_alarm_enabled = self.alarm_manager.is_alarm_enabled()
        self.assertFalse(is_alarm_enabled)



if __name__ == '__main__':
    unittest.main()

