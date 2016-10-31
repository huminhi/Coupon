'''
Created on Jul 11, 2012

@author: KhoaTran
'''

from lunex.common.v2.services import utils, ServiceNotLoad

class AtsObject(utils.DictObject):
    __service = None
    __entity_user = None
    
    class DoesNotExist(Exception):
        pass
    
    class AlreadyExist(Exception):
        pass
    
    @staticmethod
    def get_pos_service():
        '''
        Safe way to get ATS service.
        '''
        if AtsObject.__service is None:
            raise ServiceNotLoad
        
        return AtsObject.__service
    
    @staticmethod
    def load_ats_service(entity_user, url='', logger_func=None, get_srv_func=None, reload=False):
        '''
        Load POS service before being able to using it.
         - entity_user: Entity that uses the service
         - url: URL of ATS service
         - logger_func: Hook function used to log request and response of service
         - get_srv_func: User-defined function to get POS service. 
         It will skip "url" and "logger_func" parameters.
         - reload: Reload the service.   
        '''
        if AtsObject.__service is None or reload:
            if get_srv_func is None:
                srv = utils.ServiceLoader.get_pos_service(entity_user, url, logger_func)
            else:
                srv = get_srv_func(entity_user)
                
            AtsObject.__service = srv
            AtsObject.__entity_user = entity_user
            
class Entity(AtsObject):
    def __init__(self, **kwargs):
        self.Accounts = []
        self.AcctNum = ''
        self.CompanyId = 0
        self.Id = 0
        self.InstantTransfer = False
        self.Internal = False
        self.Level = 0
        self.Manager = ''
        self.Path = ''
        self.Status = ''
        
        self.set_value(**kwargs)
    
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.AcctNum = utils.get_str(self.AcctNum)
        self.CompanyId = utils.get_int(self.CompanyId)
        self.Id = utils.get_int(self.Id)
        self.InstantTransfer = utils.get_boolean(self.InstantTransfer)
        self.Internal = utils.get_boolean(self.Internal)
        self.Level = utils.get_int(self.Level)
        self.Manager = utils.get_str(self.Manager)
        self.Path = utils.get_str(self.Path)
        self.Status = utils.get_str(self.Status)
        self.Accounts = []
        for acct in kwargs['Accounts']:
            acct = Account(**acct)
            self.Accounts.append(acct)
    
class Account(AtsObject):
    ACCT_POSTPAID = 'POSTPAID'
    ACCT_PREPAID = 'PREPAID'
    ACCT_POSTPAID_BANK = 'POSTPAID_BANK'
    ACCT_PREPAID_BANK = 'PREPAID_BANK'
    
    def __init__(self, **kwargs):
        self.AcctType = ''
        self.Balance = 0
        self.Currency = ''
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.AcctType = utils.get_str(self.AcctType)
        self.Balance = utils.get_decimal(self.Balance)
        self.Currency = utils.get_str(self.Currency)