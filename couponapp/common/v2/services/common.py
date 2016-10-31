'''
Created on Sep 19, 2011

@author: KhoaTran
'''

class HandledException(Exception):
    STR_DEFAULT = 'An exception has been raised.'
    def __str__(self):
        if len(self.args) > 0:
            return self.args
        return self.STR_DEFAULT