import configparser


class Config_manager(object):

    def __init__(self, config_path):
        self.__config_path = config_path
        self.__config = configparser.ConfigParser(allow_no_value=True)
        self.__config.read(config_path)

    def get_config_file(self):
        return self.__config

    def get_properties_group(self, group_name):
        if group_name in self.__config:
            return self.__config[group_name]
        else:
            return None

    def prepare_general_config(self):
        if 'GENERAL' not in self.__config:
            self.__config['GENERAL'] = {}
            self.__config['GENERAL']['base_url'] = "http://127.0.0.1"
            self.__config['GENERAL']['port'] = "5000"

            self.save()

    def prepare_time_config(self):
        if 'TIME' not in self.__config:
            self.__config['TIME'] = {}
            self.__config.set('TIME','; Check http://php.net/manual/es/timezones.php for timezones format')
            self.__config['TIME']['time_zone'] = "Europe/Madrid"
            self.__config['TIME']['server'] = "2.europe.pool.ntp.org"

            self.save()

    def prepare_alarm_config(self):
        if 'ALARM' not in self.__config:
            self.__config['ALARM'] = {}
            self.__config['ALARM']['alarm_enabled'] = "no"
            self.__config['ALARM']['alarm_hour'] = "00"
            self.__config['ALARM']['alarm_minute'] = "00"
            self.__config['ALARM']['alarm_minute'] = "00"
            self.__config['ALARM']['default_alarm_path'] = "./resources/default_alarm.ogg"
            self.__config['ALARM']['default_station_url'] = ""

            self.save()

    def prepare_all_configs(self):
        self.prepare_general_config()
        self.prepare_time_config()
        self.prepare_alarm_config()

    def save(self):
        with open(self.__config_path, 'w') as configfile:
            self.__config.write(configfile)