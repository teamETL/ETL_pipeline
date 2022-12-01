from pythonjsonlogger import jsonlogger
from pytz import timezone
import datetime
import json_log_formatter

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

class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra['message'] = message
        #extra['request'] = record
        # extra['levelname'] = record.__dict__['levelname']
        # extra['name'] = record.__dict__['name']
        # extra['lineno'] = record.__dict__['lineno']
        # extra['filename'] = record.__dict__['filename']
        # extra['pathname'] = record.__dict__['pathname']
        # extra['created'] = record.__dict__['created']
        request = extra.pop('request', None)
        if request:
            extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
        return extra


