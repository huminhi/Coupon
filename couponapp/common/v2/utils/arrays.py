'''
Created on Jan 17, 2012

@author: KhoaTran
'''

class ArrayUtils(object):
    @staticmethod
    def replace_array(from_array, replace_array_values):
        temp_array = list(from_array)
        arr = [val for val in from_array]
        for item in replace_array_values:
            try:
                i = temp_array.index(item[0])
                temp_array[i] = '___'
                arr[i] = item[1]
            except:
                pass
            
        return arr