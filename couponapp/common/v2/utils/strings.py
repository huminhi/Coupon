'''
Created on Jan 17, 2012

@author: KhoaTran
'''
import re
from django.utils.encoding import smart_str

control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))
control_char_re = re.compile('[%s]' % re.escape(control_chars),re.UNICODE)

class StringUtils(object):
    @staticmethod
    def remove_control_chars(str):
        return control_char_re.sub(u'', smart_str(str))
    
    @staticmethod
    def remove_nonascii_chars(s):
        if (not isinstance(s, (str,unicode))):
            return s
        tmp = ''
        for c in s:
            tmp += c if ord(c) < 128 else '_'
        return tmp
    
    @staticmethod
    def remove_nonnum_chars(s):
        tmp = ''
        for c in s:
            tmp += c if c in '1234567890' else ''
        return tmp
    
    @staticmethod
    def format_phone_number(str, format='({0}) {1}-{2}', mask1='', mask2='', mask3=''):
        """
        Format: ({0}) {1}-{2} or {0}-{1}-{2}
        """
        if str:
            if len(str) == 10:
                return format.format(mask1 if mask1 else str[:3], 
                                     mask2 if mask2 else str[3:6],
                                     mask3 if mask3 else str[6:10])
            if len(str) == 11:
                return format.format(mask1 if mask1 else str[:3],
                                     mask2 if mask2 else str[3:6],
                                     mask3 if mask3 else str[6:11])
            
        return str
    
    @staticmethod
    def format_cc_number(str, format='{0}-{1}-{2}-{3}'):
        if str:
            if len(str) > 12:
                return '{0}-{1}-{2}-{3}'.format(str[:4], str[4:8], str[8:12], str[12:])
            
        return str
            