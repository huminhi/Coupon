'''
Created on Jan 17, 2012

@author: KhoaTran
'''

import locale

class PrettyFloat(float):
    def __repr__(self):
        return '%.15g' % self

class NumberUtils(object):
    @staticmethod
    def __format_currency_inner(val, decimal_places=0):
        return "$" + locale.format("%0.{0}f".format(decimal_places), val, grouping=True)
    
    @staticmethod
    def format_currency(val, decimal_places=2):
        try:
            if val == None:
                return None;
            
            if val < 0:
                txt = '(%s)' % NumberUtils.__format_currency_inner(-val, decimal_places);
            else:
                txt = NumberUtils.__format_currency_inner(val, decimal_places);
            return txt;
        except Exception:
            return val
        
    @staticmethod
    def format_number(val, decimal_places = 0):
        try:
            if val == None:
                return None;
            
            if decimal_places > 0:
                txt = locale.format("%0.{0}f".format(decimal_places), val, grouping=True)
            else:
                txt = locale.format("%d", val, grouping=True)
            return txt
        except Exception:
            return val;
    
    @staticmethod
    def format_percentage(decimal, decimal_places = 2):
        format_str = '0.{0}%'.format(decimal_places)
        return format(decimal, format_str);
    
    @staticmethod
    def get_safe_value(func, obj, default='#N/A'):
        try:
            return func(obj)
        except Exception:
            return default