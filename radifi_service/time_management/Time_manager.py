import datetime
import os
import subprocess

class Time_manager(object):

    def __init__(self, config):
        self.__config = config
        self.__config_time = self.__config.get_properties_group('TIME')

    def check_root_privileges(self):
        return os.geteuid() == 0

    def claim_root_privileges(self):
        subprocess.call(['sudo', 'python3'])

    def update_system_time(self):
        time_zone = self.__config_time['time_zone']
        ntp_server = self.__config_time['server']
        os.environ['TZ'] = time_zone
        os.system("ntpdate -s  " + ntp_server)

    def get_current_time(self):
        time_from_system = datetime.datetime.now()
        return time_from_system.strftime("%H:%M:%S")

