import threading
import time

import schedule

from scripts import launch_alarm_script


class Alarm_manager(object):

    def __init__(self,config):
        self.__scheduler_thread = None
        self.__config = config
        self.__config_alarm = self.__config.get_properties_group('ALARM')
        self.set_current_alarm(self.__config_alarm['alarm_hour'],self.__config_alarm['alarm_minute'])
        self.toggle_alarm(self.__config_alarm.getboolean('alarm_enabled'))

    def get_current_alarm(self):
        return self.__hour_to_set,self.__minute_to_set

    def set_current_alarm(self, hour_to_set,minute_to_set):
        self.__hour_to_set = hour_to_set
        self.__minute_to_set = minute_to_set

    def is_alarm_enabled(self):
        return self.__is_alarm_enabled()

    def __clear_scheduler(self):
        self.__scheduler_thread.clear()
        self.__scheduler_thread = None
        schedule.clear()

    def __trigger_scheduler(self):
        scheduler_thread = threading.Event()
        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not scheduler_thread.is_set():
                    schedule.run_pending()
                    time.sleep(2)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        self.__scheduler_thread = scheduler_thread

    def __enable_alarm(self):
        time_parsed = str(self.__hour_to_set)+":"+str(self.__minute_to_set)
        schedule.every().day.at(time_parsed).do(Alarm_manager.execute_alarm)
        self.__trigger_scheduler()


    def toggle_alarm(self, is_alarm_enabled):
        self.__is_alarm_enabled = is_alarm_enabled
        if self.__scheduler_thread != None:
            self.__clear_scheduler()
        if is_alarm_enabled:
            self.__enable_alarm()

    def save_status(self):
        self.__config.save()

    def execute_alarm(self):
        general_config = self.__config.get_properties_group('GENERAL')
        url_to_call = general_config['base_url']
        port = general_config['port']
        launch_alarm_script.execute(url_to_call, port)
