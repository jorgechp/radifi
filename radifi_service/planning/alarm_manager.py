"""
This module manages the Radifi Alarm System to perform the following operations:

    * CRUD operations over the alarm.
    * Enable/disable the alarm
    * Return information about the current status of the Alarm.

Note that this module doesn't plays the alarm. This functionality is covered
by the music package. But this method includes a trigger to tell the Player to
start playing the alarm (see AlarmManager.execute_alarm() ).

"""

import threading
import time
import schedule

from scripts import launch_alarm_script


class AlarmManager:
    """
    AlarmManager class represents the Alarm Management System.
    """

    def __init__(self, config):
        """
        Constructor. A ConfigManager instance is require to instantiate AlarmManager class.

        ARGUMENTS:
            :param config: The ConfigManager instance.
            :type config: ConfigManager
        """
        self._hour_to_set = 0
        self._minute_to_set = 0
        self.__is_alarm_enabled = False
        self._scheduler_thread = None
        self._config = config
        self._config_alarm = self._config.get_properties_group('ALARM')
        self.set_current_alarm(self._config_alarm['alarm_hour'], self._config_alarm['alarm_minute'])
        self.toggle_alarm(self._config_alarm.getboolean('alarm_enabled'))

    def get_current_alarm(self):
        """
        Get the current hour and minute set to the alarm.

        ARGUMENTS
            :return: A tuple with the hour and the minute.
            :rtype: tuple
        """
        return self._hour_to_set, self._minute_to_set, self.__is_alarm_enabled

    def get_current_alarm_radio_station(self):
        """
        Get the current alarm station
        :return: A tuple with the name and the url of the radio station.
        :rtype: tuple
        """
        station_name = self._config_alarm['alarm_station_name']
        station_url = self._config_alarm['alarm_station_url']
        return station_name, station_url

    def set_current_alarm_radio_station(self, station_name: str,station_url: str):
        """
        Set the alarm station
        :param station_name: The name of the station
        :param station_url:  The url to the station
        :return:
        """
        self._config_alarm['alarm_station_name'] = station_name
        self._config_alarm['alarm_station_url'] = station_url
        return True


    def set_current_alarm(self, hour_to_set: int, minute_to_set: int):
        """
        Set the current alarm.

        ARGUMENTS
            :param hour_to_set: The hour to be set
            :type hour_to_set: int
            :param minute_to_set: The minute to be set.
            :type minute_to_set: int

        """
        self._hour_to_set = hour_to_set
        self._minute_to_set = minute_to_set

    def is_alarm_enabled(self):
        """
        Checks whether the alarm is enabled or disabled.
        RETURN
            :return: True if the alarm is enabled, False otherwise.
            :rtype: bool
        """
        return self.__is_alarm_enabled

    def _clear_scheduler(self):
        """
        Clear the Scheduler.
        """
        self._scheduler_thread.clear()
        self._scheduler_thread = None
        schedule.clear()

    def _trigger_scheduler(self, interval=2):
        """
        Trigger the Scheduler. Starting it in a new Thread. There is an interval of time
        needed to poll continuously the scheduler to check if its time to
        play the alarm.

        ARGUMENTS
            :param interval: The interval of time between polling the scheduler.

        RETURN
            :rtype interval: int
        """
        scheduler_thread = threading.Event()

        class ScheduleThread(threading.Thread):
            """
            This internal class handle the Thread to poll the scheduler.

            Based on run_continuously() method from schedule project.
            https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py
            """
            @classmethod
            def run(cls):
                while not scheduler_thread.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        self._scheduler_thread = scheduler_thread

    def _enable_alarm(self):
        """
        Turns the alarm on. This method is intended to be private.
        """
        time_parsed = str(self._hour_to_set) + ":" + str(self._minute_to_set)
        schedule.every().day.at(time_parsed).do(AlarmManager.execute_alarm)
        self._trigger_scheduler()

    def toggle_alarm(self, is_alarm_enabled):
        """
        Enables or disables the alarm.

        ARGUMENTS

        :param is_alarm_enabled: True if the alarm should be enabled.
            False if the alarm should be disabled.
        """

        self.__is_alarm_enabled = is_alarm_enabled
        if self._scheduler_thread is not None:
            self._clear_scheduler()
        self._config_alarm['alarm_enabled'] = "no"
        if is_alarm_enabled:
            self._enable_alarm()
            self._config_alarm['alarm_enabled'] = "yes"


    def save_status(self):
        """
        Save the current settings.
        """
        self._config_alarm['alarm_hour'] = str(self._hour_to_set)
        self._config_alarm['alarm_minute'] = str(self._minute_to_set)
        self._config.save()

    def execute_alarm(self):
        """
        Executes the Alarm. Calling to an external script file.
        """
        general_config = self._config.get_properties_group('GENERAL')
        url_to_call = general_config['base_url']
        port = general_config['port']
        launch_alarm_script.execute(url_to_call, port)
