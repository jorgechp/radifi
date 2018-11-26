import threading
import time
import schedule

from scripts import launch_alarm_script


class AlarmManager(object):

    def __init__(self,config):
        self._scheduler_thread = None
        self._config = config
        self._config_alarm = self._config.get_properties_group('ALARM')
        self.set_current_alarm(self._config_alarm['alarm_hour'], self._config_alarm['alarm_minute'])
        self.toggle_alarm(self._config_alarm.getboolean('alarm_enabled'))

    def get_current_alarm(self):
        return self._hour_to_set, self._minute_to_set

    def set_current_alarm(self, hour_to_set,minute_to_set):
        self._hour_to_set = hour_to_set
        self._minute_to_set = minute_to_set

    def is_alarm_enabled(self):
        return self.__is_alarm_enabled()

    def _clear_scheduler(self):
        self._scheduler_thread.clear()
        self._scheduler_thread = None
        schedule.clear()

    def _trigger_scheduler(self):
        scheduler_thread = threading.Event()
        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not scheduler_thread.is_set():
                    schedule.run_pending()
                    time.sleep(2)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        self._scheduler_thread = scheduler_thread

    def _enable_alarm(self):
        time_parsed = str(self._hour_to_set) + ":" + str(self._minute_to_set)
        schedule.every().day.at(time_parsed).do(AlarmManager.execute_alarm)
        self._trigger_scheduler()


    def toggle_alarm(self, is_alarm_enabled):
        self.__is_alarm_enabled = is_alarm_enabled
        if self._scheduler_thread != None:
            self._clear_scheduler()
        if is_alarm_enabled:
            self._enable_alarm()

    def save_status(self):
        self._config.save()

    def execute_alarm(self):
        general_config = self._config.get_properties_group('GENERAL')
        url_to_call = general_config['base_url']
        port = general_config['port']
        launch_alarm_script.execute(url_to_call, port)
