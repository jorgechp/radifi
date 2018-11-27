"""
This module tests the module Config Manager.
"""
import unittest
from configparser import ConfigParser, SectionProxy

from config_manager import ConfigManager


CONFIG_FILE_URL = 'radifi_test_configuration.ini'

class ConfigManagerTest(unittest.TestCase):


    def setUp(self):
        self.config_manager = ConfigManager(CONFIG_FILE_URL)

    def test_get_config_file(self):
        config_getter = self.config_manager.get_config_file()
        self.assertIsInstance(config_getter,ConfigParser)

    def test_get_properties_group_exists(self):
        config_group_name = "ALARM"

        config_group = self.config_manager.get_properties_group(config_group_name)
        self.assertIsInstance(config_group,SectionProxy)

    def test_get_properties_group_not_exists(self):
        config_group_name = "HELLO WORLD"

        config_group = self.config_manager.get_properties_group(config_group_name)
        self.assertIsNone(config_group)

if __name__ == '__main__':
    unittest.main()
