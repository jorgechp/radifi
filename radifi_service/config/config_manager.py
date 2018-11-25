import configparser


class ConfigManager(object):

    def __init__(self, config_path):
        self._config_path = config_path
        self._config = configparser.ConfigParser(allow_no_value=True)
        self._config.read(config_path)

    def get_config_file(self):
        return self._config

    def get_properties_group(self, group_name):
        if group_name in self._config:
            return self._config[group_name]
        else:
            return None

    def prepare_general_config(self):
        if 'GENERAL' not in self._config:
            self._config['GENERAL'] = {}
            self._config['GENERAL']['base_url'] = "http://127.0.0.1"
            self._config['GENERAL']['port'] = "5000"

            self.save()

    def prepare_time_config(self):
        if 'TIME' not in self._config:
            self._config['TIME'] = {}
            self._config.set('TIME', '; Check http://php.net/manual/es/timezones.php for timezones format')
            self._config['TIME']['time_zone'] = "Europe/Madrid"
            self._config['TIME']['server'] = "2.europe.pool.ntp.org"

            self.save()

    def prepare_alarm_config(self):
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
        self.prepare_general_config()
        self.prepare_time_config()
        self.prepare_alarm_config()

    def save(self):
        with open(self._config_path, 'w') as configfile:
            self._config.write(configfile)