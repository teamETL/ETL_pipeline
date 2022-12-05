from django.apps import AppConfig
from django.conf import settings

class botConfig(AppConfig):
    name = 'bot'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import scheduler
            scheduler.start()