'''
Created on Sep 5, 2011

@author: KhoaTran
'''
import io
import urllib2
import gzip
import string
import requests
from django.utils import simplejson
from lunex.common import log, httputils
from django.http import HttpResponse
logger = log.setup_logger('json_client')

HTTP_GET = 'GET'
HTTP_POST = 'POST'
HTTP_PUT = 'PUT'
HTTP_DELETE = 'DELETE'

class ResponseNotOk(Exception):
    STR_RESPONSE_EXCEPTION = 'Response Status is not 200 or 201.'
    
    def __init__(self, message=None, response=None, content=None):
        self.response = response
        self.content = content
        self.message = message
        
    def __str__(self):
        if self.message is not None and self.message != '':
            return self.message
        elif self.response is not None:
            return '%s:%s' % (self.response.status_code,
                              self.content)
        else:
            return self.STR_RESPONSE_EXCEPTION

def call_api_json(method, url, params=None, **kwargs):
    '''
    Call internal API by JSON format.
    - method: One of 'GET, 'POST', etc.
    - url: Direct URL. eg. 'http://host/search'
    - params: A string or key-valued parameters in the body of request.
     will be formatted in JSON.
    - kwargs['exception_formatter_func']: A function to format response and content
     to present in ResponseException.
     * exception_formatter_func(response: Django Response object, content: string)
    - kwargs['lunex_user']: Will be header of POS request
    - kwargs['remote_addr']: Will be header of POS request
    '''
    tmp = params
    content_length = 0
    lunex_user = kwargs.get('lunex_user')
    remote_addr = kwargs.get('remote_addr')
    timeout = kwargs.get('timeout')
    if params:
        tmp = simplejson.dumps(params)
        content_length = len(tmp)
    
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Content-Length': str(content_length)}
    
    if lunex_user != '' and lunex_user is not None:
        headers['x_lunex_user'] = lunex_user;
    if remote_addr != '' and remote_addr is not None:
        headers['REMOTE_ADDR'] = remote_addr;
    
    content = None
    logger.debug('%s %s PARAMS: %s HEADERS: %s' % (method, url, params, headers))
    if method == 'GET':
        #try:
        #    req = urllib2.Request(url,headers={"Accept": "application/json","Accept-Encoding": "gzip, deflate"})
        #    response = urllib2.urlopen(req).read()
        #    content = gzip.GzipFile(fileobj= io.BytesIO(response), mode="rb").read()
        #    #Simulate httplib.HTTPReponse object
        #    response = HttpResponse()
        #    response.status = 200
        #except:
        #    response, content = httputils.send_json_request(method, url, tmp, headers)
        #response, content = httputils.send_json_request(method, url, tmp, headers)
        response = requests.get(url, data=params, headers=headers, timeout=timeout)
        content = response.json()
        response_status = response.status_code
    else:
        #response, content = httputils.send_json_request(method, url, tmp, headers)
        if (method == 'POST'):
            response = requests.post(url, data=tmp, headers=headers, timeout=timeout)
        elif (method == 'PUT'):
            response = requests.put(url, data=tmp, headers=headers, timeout=timeout)
        elif (method == 'DELETE'):
            response = requests.delete(url, data=tmp, headers=headers, timeout=timeout)
        content = response.json()
        response_status = response.status_code
            
    logger.debug('Response %s' % (response_status))
    logger.debug(content)
    #content = string.strip(content)
    #if len(content) > 0 and '(' == content[0]:
    #    content = content[1:-1]

    if response_status not in [200, 201]:
        formatter_func = kwargs.get('exception_formatter_func')
        formatted_msg = None
        if formatter_func:
            formatted_msg = formatter_func(response, content)
        raise ResponseNotOk(message=formatted_msg,
                            response=response, 
                            content=content)

    #if len(content) == 0:
    #if not content:
    #    return None
    
    #return simplejson.loads(content)
    return content
