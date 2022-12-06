from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, DjangoJobStore
import time
from .bots import bot_activate
from myproject.compress import compressor

def start():
    '''
    스케줄링
    '''
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('cron', minute = '*/30', name = 'auto_bot')
    def auto_bot():
        bot_activate(10)
        compressor() #압축 알고리즘 적용
    scheduler.start()