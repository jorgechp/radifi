import configparser

from os import path, error
from crontab import CronTab

CONFIG_FILE_URL = 'config/radifi_configuration.ini'
CRONTAB_FILE_URL = 'config/alarm.tab'


class Alarm_manager(object):

    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read(CONFIG_FILE_URL)
        self.__system_crontab = self.__prepare_crontab_file()
        self.__system_crontab_job = self.__prepare_crontab_job()

        if 'ALARM' not in self.__config:
            self.__config['ALARM'] = {}
            self.__config['ALARM']['alarm_enabled'] = "no"
            self.__config['ALARM']['alarm_hour'] = "00"
            self.__config['ALARM']['alarm_minute'] = "00"

            self.save_status()

        self.__config_alarm = self.__config['ALARM']
        self.toggle_alarm(self.__config_alarm.getboolean('alarm_enabled'))
        self.set_current_alarm(self.__config_alarm['alarm_hour'],self.__config_alarm['alarm_minute'])

    def __prepare_crontab_file(self):
        if path.isfile(CRONTAB_FILE_URL):
            cron_instance = CronTab(tabfile=CRONTAB_FILE_URL)
        else:
            cron_instance = CronTab()
            cron_instance.write(CRONTAB_FILE_URL)
        return cron_instance

    def __prepare_crontab_job(self):
        job_list = self.__system_crontab.lines
        num_of_jobs = len(job_list)
        if(num_of_jobs == 1):
            job_to_return = job_list[0]
        elif(num_of_jobs == 0):
            job_to_return = self.__system_crontab.new(command='./fire_alarm.py', comment='Alarm')
        else:
            raise RuntimeError('There are two or more jobs at the alarm.tab file. There must be 1 or 0.') from error
        return job_to_return


    def get_current_alarm(self):
        return self.__hour_to_set,self.__minute_to_set

    def set_current_alarm(self, hour_to_set,minute_to_set):
        self.__hour_to_set = hour_to_set
        self.__minute_to_set = minute_to_set
        self.__system_crontab_job.hour.every(self.__hour_to_set)
        self.__system_crontab_job.minute.every(self.__minute_to_set)

    def is_alarm_enabled(self):
        return self.__system_crontab_job.is_enabled()

    def toggle_alarm(self, is_alarm_enabled):
        self.__system_crontab_job.enable(is_alarm_enabled)

    def save_status(self):
        with open(CONFIG_FILE_URL, 'w') as configfile:
            self.__config.write(configfile)

    def get_cronJob(self):
        return str(self.__system_crontab_job)