'''
Created on Sep 5, 2011

@author: KhoaTran
'''
import re
import datetime
from decimal import Decimal
from lunex.common.v2.services.pos.api import PosService
from lunex.common.v2.services.ats.api import AtsService
from lunex.common.v2.services.auth.api import AuthService

class DictObject(object):
    def set_value(self, **entries):
        '''
        Fill key-valued items to properties of object
        '''
        self.__dict__.update(entries)
        
    def to_dict(self):
        result = dict([(key, value) for (key, value) in self.__dict__.iteritems() if key[:1] != '__'])
        return result

def obj_dict(d):
    '''
    From: SilentGhost @ http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
    '''
    top = type('obj', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, obj_dict(j))
        elif isinstance(j, seqs):
            setattr(top, i, 
                    type(j)(obj_dict(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top

def get_boolean(value, default_value=False):
    '''
    Convert number to integer. 
    If error occurred, default value will be returned 
    '''
    safe_value = default_value
    if value is not None and value != '':
        try:
            str_value = str(value)
            if str_value in ['1', 'True']:
                safe_value = True
            else:
                safe_value = False
        except:
            pass
    
    return safe_value

def get_int(value, default_value=0):
    '''
    Convert number to integer. 
    If error occurred, default value will be returned 
    '''
    safe_value = default_value
    if value is not None and value != '':
        try:
            safe_value = int(str(value)) 
        except:
            pass
    
    return safe_value

def get_decimal(value, default_value=0):
    '''
    Convert number to Decimal object. 
    If error occurred, default value will be returned 
    '''
    safe_value = default_value
    if value is not None and value != '':
        try:
            safe_value = Decimal(str(value)) 
        except:
            pass
    
    return safe_value

def get_str(value, default_value=''):
    '''
    Convert number to integer. 
    If error occurred, default value will be returned 
    '''
    safe_value = default_value
    if value is not None and value != '':
        try:
            safe_value = str(value) 
        except:
            pass
    
    return safe_value
    
def get_json_datetime(value, default_value=None):
    '''
    Convert date time formatted JSON string to datetime object. 
    If value is not a string, default value will be returned 
    '''
    safe_value = default_value
    if value is not None and value != '' and not(type(value) is datetime.datetime):
        try:
            safe_value = from_json_datetime(str(value))
        except:
            pass
    
    return safe_value
    
def from_json_datetime(val):
    '''
    Convert date time formatted JSON string to datetime object 
    '''
    if val == None or len(val) < 1:
        return None;    
    m = re.match("/Date\((?P<date>\d+)-(?P<hour>\d{2})(?P<min>\d{2})\)/", val);
    time_stamp = int(m.group('date')) / 1000;
    hour = int(m.group('hour'),10);
    min = int(m.group('min'),10);
    ret = datetime.datetime.utcfromtimestamp(time_stamp);
    ret = ret - datetime.timedelta(hours = hour, minutes= min); #adjust for local time
    return ret;

class ServiceLoader(object):
    @staticmethod
    def get_pos_service(entity_user, url, logger_func=None, **kwargs):
        '''
         - url: Such as "http://test-api.lunextelecom.com/"
        '''
        return PosService(entity_user, 
                          url, 
                          logger_func, **kwargs)
        
    @staticmethod
    def get_ats_service(entity_user, url, logger_func=None):
        '''
         - url: Such as "http://test-api.lunextelecom.com/"
        '''
        return AtsService(entity_user, 
                          url, 
                          logger_func)
        
    @staticmethod
    def get_auth_service(entity_user, url, logger_func=None):
        '''
         - url: Such as "http://test-api.lunextelecom.com/"
        '''
        return AuthService(entity_user, 
                           url, 
                           logger_func)