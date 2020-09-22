"""
This module manages the Radifi Time System to perform the following operations:

    * Change the System date (root privileges required).
    * Gets the current System Time.

"""

import datetime
import os
import subprocess
import sys
import time
import threading

from output.lcd.lcd_manager import LCDManager


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

    def __init__(self, config, lcd_manager: LCDManager):
        """
        Constructor.

        ARGUMENTS
            :param config: The ConfigManager instance.
            :type config: ConfigManager
        """
        self._config = config
        self._config_time = self._config.get_properties_group('TIME')
        self._lcd_manager = lcd_manager

        self._long_time_format = "%d/%m/%Y %H:%M"
        self._short_time_format = "%H:%M"

        th = threading.Thread(target=TimeManager.update_lcd_time, args=(
            self._short_time_format,
            self._long_time_format,
            self._lcd_manager
        ))
        th.start()



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

    @staticmethod
    def update_lcd_time(short_time_format: str, long_time_format: str, lcd_manager: LCDManager):
        startime = datetime.datetime.now()
        while True:
            current_time = datetime.datetime.now()
            time_formatter = short_time_format if lcd_manager.is_busy_lcd else long_time_format
            strtime = current_time.strftime(time_formatter)
            lcd_manager.print_message(strtime)

            time.sleep(60.0 - ((time.time() - startime) % 60.0))
