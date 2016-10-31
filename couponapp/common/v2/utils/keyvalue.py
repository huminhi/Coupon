'''
Created on Mar 29, 2012

@author: KhoaKhoi
'''
from types import FunctionType
from lunex.common.v2.utils.numbers import NumberUtils

class KeyValueUtils(object):
    @staticmethod            
    def get_value(obj, getter):
        value = '#N/A'
        if isinstance(getter, FunctionType):
            value = NumberUtils.get_safe_value(getter,obj)
        else:                
            if isinstance(obj, dict):
                value = obj[getter]
            else:        
                value = getattr(obj,getter)
                
        return value