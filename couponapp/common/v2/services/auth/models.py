'''
Created on Jul 11, 2012

@author: KhoaTran
'''

from decimal import Decimal
from lunex.common.v2.services import utils, ServiceNotLoad, ApiError
from lunex.common.v2.services.ats.models import Entity

class AuthObject(utils.DictObject):
    __service = None
    __entity_user = None
    
    class DoesNotExist(Exception):
        pass
    
    class AlreadyExist(Exception):
        pass
    
    @staticmethod
    def get_auth_service():
        '''
        Safe way to get Auth service.
        '''
        if AuthObject.__service is None:
            raise ServiceNotLoad
        
        return AuthObject.__service
    
    @staticmethod
    def load_auth_service(entity_user, url='', logger_func=None, get_srv_func=None, reload=False):
        '''
        Load POS service before being able to using it.
         - entity_user: Entity that uses the service
         - url: URL of Auth service
         - logger_func: Hook function used to log request and response of service
         - get_srv_func: User-defined function to get POS service. 
         It will skip "url" and "logger_func" parameters.
         - reload: Reload the service.   
        '''
        if AuthObject.__service is None or reload:
            if get_srv_func is None:
                srv = utils.ServiceLoader.get_auth_service(entity_user, url, logger_func)
            else:
                srv = get_srv_func(entity_user)
                
            AuthObject.__service = srv
            AuthObject.__entity_user = entity_user
            
class LoginToken(AuthObject):
    def __init__(self, **kwargs):
        self.Code = 0
        self.Message = ''
        self.Time = None
        self.CompanyId = 0
        self.IsChangePwd = False
        self.LastLoginTime = None
        self.Type = 0
        self.Username = ''
        self.Entity = None
        self.set_value(**kwargs)
    
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.Code = utils.get_int(self.Code)
        self.Message = utils.get_str(self.Message)
        self.Time = utils.get_json_datetime(self.Time, None)
        self.CompanyId = utils.get_int(self.CompanyId)
        self.IsChangePwd = utils.get_boolean(self.IsChangePwd)
        self.LastLoginTime = utils.get_json_datetime(self.LastLoginTime)
        self.Type = utils.get_int(self.Type)
        self.Username = utils.get_str(self.Username)
        self.Entity = Entity(**kwargs['Entity'])

    @staticmethod
    def login(username, password, **kwargs):
        login_token_dict = LoginToken.get_auth_service().login(username, password, **kwargs)
        return LoginToken(**login_token_dict)
    