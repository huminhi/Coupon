from lunex.common import log
from lunex.common.v2.services import json_client
from lunex.common.v2.services.common import HandledException

logger = log.setup_logger('customer.services')

class ServiceNotLoad(HandledException):
    STR_DEFAULT = 'Service is not loaded. Please call "load_service" before using.'
    
class ServiceNotFound(HandledException):
    STR_DEFAULT = 'Service can not be found.'

class InvalidEntityUser(HandledException):
    STR_DEFAULT = 'ExEntity object is required.'

class InvalidServiceUrl(HandledException):
    STR_DEFAULT = 'Service URL is empty.'
    
class ApiError(Exception):
    def __init__(self, code, message, url='', obj=None):
        self.Code = code
        self.Message = message
        self.code = code
        self.message = message
        self.url = url
        self.obj = obj
        
    def __str__(self):
        msg = '%s:%s' % (self.code, self.message)
        if self.url:
            msg = '[%s] %s:%s' % (self.url, self.code, self.message)
        return msg

class ApiService(object):
    def __init__(self, entity_user=None, service_url=None, logger_func=None, **kwargs):
        '''
        ApiService constructor.
        - entity_user: ExEntity thats use the service
        - service_url: Url of host
        - db_logger_func: Log by db function
        * db_logger_func(entity_user: ExEntity object, method: string,
            url: string, params: object, ret: object)
        '''
        self.logger_func = logger_func
        self.service_url = service_url
        self.entity_user = entity_user
        
        self.HTTP_GET = json_client.HTTP_GET
        self.HTTP_POST = json_client.HTTP_POST
        self.HTTP_PUT = json_client.HTTP_PUT
        self.HTTP_DELETE = json_client.HTTP_DELETE
        
    def call_service(self, method, url, params=None, **kwargs):
        if url.startswith('http') == False:
            if self.service_url is None or self.service_url == '':
                raise InvalidServiceUrl
            
            url = self.service_url + url;
        
        result = None
        try:
            result = json_client.call_api_json(method, url, params, **kwargs)
            if type(result) is dict:
                if result.get('Code', 0) < 0:
                    raise ApiError(result['Code'],
                                   result['Message'],
                                   url=url,
                                   obj=result)
        except json_client.ResponseNotOk, ex:
            logger.exception(ex)
            result = ex
            raise
        finally:    
            if self.logger_func is not None:
                self.logger_func(self.get_entity_user(), method, url, params, result, **kwargs)
        
        return result
    
    def call_service_test(self, method, url, params=None, **kwargs):
        if url.startswith('http') == False:
            if self.service_url is None or self.service_url == '':
                raise InvalidServiceUrl
            
            url = self.service_url + url;
        
        result = None
        try:
            url = 'http://v2.api.lunextelecom.com/PosService.svc/cdrs/?pin=642183186&from_date=20130620'
            result = json_client.call_api_json(method, url, params, **kwargs)
            if type(result) is dict:
                if result.get('Code', 0) < 0:
                    raise ApiError(result['Code'],
                                   result['Message'],
                                   url=url)
        except json_client.ResponseNotOk, ex:
            logger.exception(ex)
            result = ex
            raise
        finally:    
            if self.logger_func is not None:
                self.logger_func(self.get_entity_user(), method, url, params, result)
        
        return result
    
    def get_entity_user(self):
        return self.entity_user