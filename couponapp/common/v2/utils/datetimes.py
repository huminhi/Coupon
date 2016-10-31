'''
Created on Jan 17, 2012

@author: KhoaTran
'''

import calendar
import re
from datetime import datetime, timedelta

class DateTimeUtils(object):
    @staticmethod
    def from_dotnet_datetime(val):
        if val == None or len(val) < 1:
            return None;    
        m = re.match("/Date\((?P<date>\d+)-(?P<hour>\d{2})(?P<min>\d{2})\)/", val)
        time_stamp = int(m.group('date')) / 1000
        hour = int(m.group('hour'),10)
        min = int(m.group('min'),10)
        ret = datetime.utcfromtimestamp(time_stamp)
        ret = ret - timedelta(hours = hour, minutes= min) #adjust for local time
        return ret
    
    @staticmethod
    def get_today():
        now = datetime.now()
        return datetime(year=now.year, month=now.month, day=now.day)
    
    @staticmethod
    def get_end_today():
        now = datetime.now()
        return datetime(year=now.year, month=now.month, day=now.day, 
                        hour=23, minute=59, second=59)
    
    @staticmethod
    def get_from_to_date(from_date='', to_date='', period=30, date_format='%m/%d/%Y'):
        if not to_date:
            now = datetime.now()
            to_date = datetime(now.year, now.month, now.day)
        else:
            to_date = datetime.strptime(to_date, date_format)
            
        if not from_date:
            from_date = to_date - timedelta(days=period)
            from_date = from_date.strftime(date_format)
    
        to_date = datetime.strptime(to_date.strftime(date_format) + ' 23:59:59', date_format + ' %H:%M:%S')
        from_date = datetime.strptime(from_date, date_format)
        
        return from_date, to_date
    
    @staticmethod
    def get_from_to_month(months):
        date_iter = datetime.now()
        _, end = calendar.monthrange(date_iter.year, date_iter.month)
        to_date = datetime(year=date_iter.year, month=date_iter.month, day=end,
                             hour=23, minute=59, second=59)
        
        for _ in range(months-1):
            summary_date = datetime(year=date_iter.year, 
                                    month=date_iter.month, 
                                    day=1)
            date_iter = summary_date - timedelta(days=1)
        from_date = datetime(year=date_iter.year, 
                             month=date_iter.month, 
                             day=1)
        
        return from_date, to_date
    
    @staticmethod
    def get_months(months):
        date_iter = datetime.now()
        result = []
        for _ in range(months):
            summary_date = datetime(year=date_iter.year, 
                                    month=date_iter.month, 
                                    day=1)
            date_iter = summary_date - timedelta(days=1)
            result.insert(0, summary_date)
        
        return result
    
    @staticmethod
    def get_from_date(str, date_format='%m/%d/%Y'):
        try:
            return datetime.strptime(str, date_format)
        except:
            return None
    
    @staticmethod    
    def get_to_date(str, date_format='%m/%d/%Y'):
        try:
            str += ' 23:59:59'
            return datetime.strptime(str, date_format + ' %H:%M:%S')
        except:
            return None
    
    @staticmethod
    def format_date(val, format='%m/%d/%Y', default=''):
        return DateTimeUtils.__inner_format_date(val, format, default)
    
    @staticmethod
    def format_datetime(val, format='%m/%d/%Y %H:%M:%S', default=''):
        return DateTimeUtils.__inner_format_date(val, format, default)
    
    @staticmethod
    def format_longdate(val, format='%b %d, %Y', default=''):
        return DateTimeUtils.__inner_format_date(val, format, default)
    
    @staticmethod
    def format_longdatetime(val, format='%b %d, %Y %H:%M:%S', default=''):
        return DateTimeUtils.__inner_format_date(val, format, default)
    
    @staticmethod
    def __inner_format_date(val, format, default=''):
        return val.strftime(format) if val else default
