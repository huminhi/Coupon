'''
Created on Jul 11, 2012

@author: KhoaTran
'''

from lunex.common import log
from lunex.common.v2 import services

logger = log.setup_logger('customer.services.auth.api') 

class AuthService(services.ApiService):
    '''
    Authentication Service
    '''
    AUTH_SERVICE = 'AuthService.svc/'
    
    def __init__(self, entity_user, service_url=None, logger_func=None):
        super(AuthService, self).__init__(None, service_url, logger_func)
        
    def login(self, username, password, **kwargs):
        
        url = AuthService.AUTH_SERVICE + 'login?companyid={company_id}'
        company_id = kwargs.get('company_id') if kwargs.get('company_id') else ''
        
        url = url.format(company_id=company_id)
        result = self.call_service(self.HTTP_POST, url, params={'Username': username,
                                                                'Password': password})
        
        return result
    
    def get_entity_user(self):
        return self.entity_user if self.entity_user else 'AuthService'