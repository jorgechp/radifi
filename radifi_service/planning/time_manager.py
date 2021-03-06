"""
This module manages the Radifi Time System to perform the following operations:

    * Change the System date (root privileges required).
    * Gets the current System Time.

"""

import datetime
import os
import subprocess
import sys


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

    def _set_system_time_linux(self, time_tuple: tuple):
        """
        Updates the system time on a Linux OS.
        """

        import ctypes.util
        import time

        # /usr/include/linux/time.h:
        #
        # define CLOCK_REALTIME                     0
        CLOCK_REALTIME = 0

        # /usr/include/time.h
        #
        # struct timespec
        #  {
        #    __time_t tv_sec;            /* Seconds.  */
        #    long int tv_nsec;           /* Nanoseconds.  */
        #  };
        class timespec(ctypes.Structure):
            _fields_ = [("tv_sec", ctypes.c_long),
                        ("tv_nsec", ctypes.c_long)]

        librt = ctypes.CDLL(ctypes.util.find_library("rt"))

        ts = timespec()
        ts.tv_sec = int(time.mktime(datetime.datetime(*time_tuple[:6]).timetuple()))
        ts.tv_nsec = time_tuple[6] * 1000000  # Millisecond to nanosecond

        # http://linux.die.net/man/3/clock_settime
        librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))

    def _set_system_time_windows(self, time_tuple: tuple):
        """
        Updates the system time on a Windows OS.
        """

        import pywin32
        # http://timgolden.me.uk/pywin32-docs/win32api__SetSystemTime_meth.html
        # pywin32.SetSystemTime(year, month , dayOfWeek , day , hour , minute , second , millseconds )
        dayOfWeek = datetime.datetime(time_tuple).isocalendar()[2]
        pywin32.SetSystemTime(time_tuple[:2] + (dayOfWeek,) + time_tuple[2:])

    def set_system_time(self, year: int, month: int, day: int, hour: int, minute: int) -> None:
        """
        Updates the system time. It's implemented for Linux and Windows.
        """

        time_tuple = (year,  # Year
                      month,  # Month
                      day,  # Day
                      hour,  # Hour
                      minute,  # Minute
                      0,  # Second
                      0,  # Millisecond
                      )
        if sys.platform == 'linux2':
            self._set_system_time_linux(time_tuple)
        elif sys.platform=='win32':
            self._set_system_time_windows(time_tuple)



