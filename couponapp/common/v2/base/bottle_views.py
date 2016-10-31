'''
Created on Jun 24, 2013

@author: KhoaTran
'''

import bottle
from lunex.common import log
from lunex.common.v2.base.bottle_mixins import BottleXmlResponseMixin,\
    BottleJsonResponseMixin
from lunex.common.v2.utils.bottle_requests import RequestHeaderUtils

logger = log.setup_logger('common.v2.base.bottle_views')

class BottleRestView(BottleXmlResponseMixin, BottleJsonResponseMixin):
    class HandledException(Exception):
        def __init__(self, code, message):
            self.Code = code
            self.Message = message
    '''
    A view supports REST.
    '''
    
    def __init__(self, app, url):
        self.app = app
        self.url = url
        
        self.app.route(self.url, 'GET', self.get)
        self.app.route(self.url, 'POST', self.post)
        self.app.route(self.url, 'PUT', self.put)
        self.app.route(self.url, 'DELETE', self.delete)
        
        self.request = bottle.request
            
    def render_to_response(self, context, **response_kwargs):
        accept, _ = RequestHeaderUtils.get_accept_content_type(self.request, 
                                                               response_kwargs.get('default_accept', 'json'),
                                                               response_kwargs.get('default_content', 'json')) 
        if response_kwargs.has_key('default_accept'):
            del response_kwargs['default_accept']
        if response_kwargs.has_key('default_content'):
            del response_kwargs['default_content']
        if accept == 'xml':
            response_kwargs['xml_clean'] = True
            return BottleXmlResponseMixin.render_to_response(self, context, **response_kwargs)
        else:
            return BottleJsonResponseMixin.render_to_response(self, context, **response_kwargs)
        
    def get_context_data(self, **kwargs):
        return {
            'params': kwargs
        }
        
    def get_default_accept_content(self):
        return 'json', 'json'
        
    def get(self, *args, **kwargs):
        return self.do_work(bottle.request, self.do_get, *args, **kwargs)
    
    def post(self, *args, **kwargs):
        return self.do_work(bottle.request, self.do_post, *args, **kwargs)
    
    def put(self, *args, **kwargs):
        return self.do_work(bottle.request, self.do_put, *args, **kwargs)
    
    def delete(self, *args, **kwargs):
        return self.do_work(bottle.request, self.do_delete, *args, **kwargs)
    
    def do_get(self, request, *args, **kwargs):
        return {}
    
    def do_post(self, request, *args, **kwargs):
        return {}
    
    def do_put(self, request, *args, **kwargs):
        return {}
    
    def do_delete(self, request, *args, **kwargs):
        return {}
    
    def do_work(self, request, httpmethod_func, *args, **kwargs):
        try:
            default_accept, default_content = self.get_default_accept_content()
            self.context = self.get_context_data(**kwargs)
            self.context['method'] = request.method.lower()
            self.context['params'] = RequestHeaderUtils.extract_request_by_content_type(request, 
                                                                                        default_accept=default_accept, 
                                                                                        default_content=default_content)
            
            kwargs['context'] = self.context
            self.data = httpmethod_func(request, *args, **kwargs)
            resp = self.render_to_response(self.context,
                                           default_accept=default_accept, 
                                           default_content=default_content)
        except BottleRestView.HandledException, ex:
            logger.error('RestView Exception="%s" Data=%s' % (str(ex), str(self.data)[:255]))
            logger.exception(ex)
            self.data = {'Code': ex.Code,
                         'HasError': True,
                         'Message': ex.Message}
            
            context = self.get_context_data(**kwargs)
            resp = self.render_to_response(context, status=400,
                                               default_accept=default_accept, 
                                               default_content=default_content)
        except Exception, ex:
            logger.error('RestView Exception="%s" Data=%s' % (str(ex), str(self.data)[:255]))
            logger.exception(ex)
            #Overwrite data to get Error Response
            self.data = {'Code': -1,
                         'HasError': True,
                         'Message': str(ex)}
            
            context = self.get_context_data(**kwargs)
            resp = self.render_to_response(context, status=400,
                                               default_accept=default_accept, 
                                               default_content=default_content)
            
        return resp