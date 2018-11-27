"""
This module manages the Radifi Time System to perform the following operations:

    * Change the System date (root privileges required).
    * Gets the current System Time.

"""

import datetime
import os
import subprocess


def check_root_privileges():
    """
    Checks if the current user has root privileges on the OS.
    It's neccesary to be on a Unix based operative system.

    RETURN
        :return: True if the user has root privileges, False otherwise.
    """
    return os.name != 'nt' and os.geteuid() == 0 #Check if OS is not Windows (os.name = 'nt')


def claim_root_privileges():
    """
    Claims for root privileges for the current user.
    """
    subprocess.call(['sudo', 'python3'])


def get_current_time():
    """
    Gets the current OS date.

    RETURN
        :return: The current date, formated as a string.
        :rtype: string
    """
    time_from_system = datetime.datetime.now()
    return time_from_system.strftime("%H:%M:%S")


class TimeManager:
    """
    The class TimeManager handles the communication with the Operative Systems in respect
    of changing and getting the current System date.
    """

    def __init__(self, config):
        """
        Constructor.

        ARGUMENTS
            :param config: The ConfigManager instance.
            :type config: ConfigManager
        """
        self._config = config
        self._config_time = self._config.get_properties_group('TIME')

    def update_system_time(self):
        """
        Updates the system time using a NTP server.
        You can change the default NTP server and the timeZone at the configuration file.

        """
        time_zone = self._config_time['time_zone']
        ntp_server = self._config_time['server']
        os.environ['TZ'] = time_zone
        os.system("ntpdate -s  " + ntp_server)
