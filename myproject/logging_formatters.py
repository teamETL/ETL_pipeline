from pythonjsonlogger import jsonlogger
from pytz import timezone
import datetime


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, extra):
        
        super(CustomJsonFormatter, self).add_fields(log_record, record, extra)
        
        # if log_record["message"]
        
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            
            log_record['timestamp'] = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%dT, %H:%M:%S.%fZ')

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        log_record['environment'] = 'django'


