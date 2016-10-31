'''
Created on Jan 17, 2012

@author: KhoaTran
'''
from django import http
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lunex.common import log
from lunex.common.v2.base.base_views import View
from lunex.common.v2.base.mixins import XmlResponseMixin, JsonResponseMixin
from lunex.common.v2.utils.requests import RequestHeaderUtils

logger = log.setup_logger('common.v2.base.views')

class AuthenticatedView(View):
    '''
    A view that need to authenticate and check permission.
    '''
    permissions = []
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthenticatedView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        return {
            'params': kwargs
        }
        
    def get(self, request, *args, **kwargs):
        'Default HTTP Method of View'
        return self.do_work(request, self.do_get, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.do_work(request, self.do_post, *args, **kwargs)
    
    def do_get(self, request, *args, **kwargs):
        return {}
    
    def do_post(self, request, *args, **kwargs):
        return {}
    
    def do_work(self, request, httpmethod_func, *args, **kwargs):
        for perm in self.permissions:
            if not request.user.has_perm(perm):
                response = http.HttpResponseForbidden()
                break
        else:
            self.context = self.get_context_data(**kwargs)
            self.data = httpmethod_func(request, *args, **kwargs)
            if isinstance(self.data, http.HttpResponse):
                response = self.data
            else:
                self.context['data'] = {'Code': 0,
                                        'HasError': False,
                                        'Message':''}
                if type(self.data) is not dict:
                    self.context['data'] = self.data
                else:
                    self.context['data'].update(self.data)
                    #for legacy compatible
                    self.context.update(self.data)
                self.context['method'] = request.method.lower()
                response = self.render_to_response(self.context)
        
        return response

class RestView(JsonResponseMixin, XmlResponseMixin, View):
    class HandledException(Exception):
        def __init__(self, code, message):
            self.Code = code
            self.Message = message
            
    '''
    A view supports REST.
    '''
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
            return XmlResponseMixin.render_to_response(self, context, **response_kwargs)
        else:
            return JsonResponseMixin.render_to_response(self, context, **response_kwargs)
       
    def get_context_data(self, **kwargs):
        return {
            'params': kwargs
        }
        
    def get_default_accept_content(self):
        return 'json', 'json'
        
    def get(self, request, *args, **kwargs):
        return self.do_work(request, self.do_get, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.do_work(request, self.do_post, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.do_work(request, self.do_put, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.do_work(request, self.do_delete, *args, **kwargs)
    
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
            if isinstance(self.data, http.HttpResponse):
                response = self.data
            else:
                response = self.render_to_response(self.context,
                                                   default_accept=default_accept, 
                                                   default_content=default_content)
        except RestView.HandledException, ex:
            logger.error('RestView Exception="%s" Data=%s' % (str(ex), str(self.data)[:255]))
            logger.exception(ex)
            self.data = {'Code': ex.Code,
                         'HasError': True,
                         'Message': ex.Message}
            
            context = self.get_context_data(**kwargs)
            response = self.render_to_response(context, status=400,
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
            response = self.render_to_response(context, status=400,
                                               default_accept=default_accept, 
                                               default_content=default_content)
            
        response['Content-Length'] = len(response.content)
        
        return response
