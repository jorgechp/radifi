import configparser

CONFIG_FILE_URL = 'config/radifi_configuration.ini'


class Alarm_manager(object):

    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read(CONFIG_FILE_URL)

        if 'ALARM' not in self.__config:
            self.__config['ALARM'] = {}
            self.__config['ALARM']['alarm_enabled'] = "no"
            self.__config['ALARM']['current_alarm'] = "00:00:00"

            self.save_status()

        self.__config_alarm = self.__config['ALARM']
        self.toggle_alarm(self.__config_alarm.getboolean('alarm_enabled'))
        self.set_current_alarm(self.__config_alarm['current_alarm'])

    def get_current_alarm(self):
        return self.__current_alarm

    def set_current_alarm(self, alarm_to_set):
        self.__current_alarm = alarm_to_set

    def is_alarm_enabled(self):
        return self.__is_alarm_enabled

    def toggle_alarm(self, is_alarm_enabled):
        self.__is_alarm_enabled = is_alarm_enabled

    def save_status(self):
        with open(CONFIG_FILE_URL, 'w') as configfile:
            self.__config.write(configfile)
