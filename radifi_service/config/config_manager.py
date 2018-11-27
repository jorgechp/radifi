"""
This module deals with the Configuration settings handling.
Its generate a default config file, load properties
and save new settings.

A configuration file contains three groups:

    * GENERAL settings: Related to the host and the port.
    * TIME: Configuration of the NTP server used to update the system time.
    * ALARM: Configures the Alarm.
"""


import configparser
from configparser import ConfigParser


class ConfigManager:
    """
    ConfigManager handle all the functionality related with the configuration
    settings.

        * Read configuration
        * Update configuration
        * Save configuration
        * Generate default configuration.
    """

    _config_path: str
    _config: ConfigParser

    def __init__(self, config_path: str):
        """
        Constructor of the class.

        ARGUMENTS:
            :param config_path: The path to the configuration file
            :type config_path: str

        """
        self._config_path = config_path
        self._config = configparser.ConfigParser(allow_no_value=True)
        self._config.read(config_path)

    def get_config_file(self):
        """
        Get the path to the configuration file.
        :return: The path to the configuration file.
        :rtype: str
        """
        return self._config

    def get_properties_group(self, group_name: str):
        """
        Get a dictionary with all the settings related to a group.

        :param group_name: The group whose settings we wish to get.
        :type group_name: str
        :return: A dictionary.
        :rtype: ConfigParser
        """
        if group_name in self._config:
            return self._config[group_name]

        return None

    def prepare_general_config(self):
        """
        Generates default settings for the GENERAL group.
        """
        if 'GENERAL' not in self._config:
            self._config['GENERAL'] = {}
            self._config['GENERAL']['base_url'] = "http://127.0.0.1"
            self._config['GENERAL']['port'] = "5000"

            self.save()

    def prepare_time_config(self):
        """
        Generates default settings for the TIME group.
        """
        if 'TIME' not in self._config:
            self._config['TIME'] = {}
            self._config.set('TIME',
                             '; Check http://php.net/manual/es/timezones.php for timezones format')
            self._config['TIME']['time_zone'] = "Europe/Madrid"
            self._config['TIME']['server'] = "2.europe.pool.ntp.org"

            self.save()

    def prepare_alarm_config(self):
        """
        Generates default settings for the ALARM group.
        """
        if 'ALARM' not in self._config:
            self._config['ALARM'] = {}
            self._config['ALARM']['alarm_enabled'] = "no"
            self._config['ALARM']['alarm_hour'] = "00"
            self._config['ALARM']['alarm_minute'] = "00"
            self._config['ALARM']['alarm_minute'] = "00"
            self._config['ALARM']['default_alarm_path'] = "./resources/default_alarm.ogg"
            self._config['ALARM']['default_station_url'] = ""

            self.save()

    def prepare_all_configs(self):
        """
        Generates default settings for all the groups.
        """
        self.prepare_general_config()
        self.prepare_time_config()
        self.prepare_alarm_config()

    def save(self):
        """
        Save the settings into disk.
        """
        with open(self._config_path, 'w') as configfile:
            self._config.write(configfile)
