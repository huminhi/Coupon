'''
Created on Jan 17, 2012

@author: KhoaKhoi
'''
import simplejson
from lunex.common import log
from lunex.common.v2.base.exceptions import ParameterExtractFailed
from lunex.common.v2.utils.converters import Xml2Json

logger = log.setup_logger('common.v2.utils.request_utils')

class RequestHeaderUtils(object):
    @staticmethod
    def get_accept_content_type(request, default_accept='json', default_content='json'): 
        accept, content = default_accept, default_content
        accept_type = request.META.get('HTTP_ACCEPT', '').lower()
        content_type = request.META.get('CONTENT_TYPE', '').lower()
        
        if content_type in ['application/json', ]:
            content = 'json'
        elif content_type in ['text/xml', 'application/xml']:
            content = 'xml'
        elif content_type in ['post', ]:
            content = 'post'
        
        if accept_type == '' and content != 'post':
            accept = content
        else:
            if accept_type in ['application/json']:
                accept = 'json'
            elif accept_type in ['text/xml', 'application/xml']:
                accept = 'xml'
            
        return accept.lower(), content.lower()
    
    @staticmethod
    def extract_header(request):
        args = {}
        for k, v in request.META.iteritems():
            if k.startswith('HTTP_'):
                key = k[5:].lower().capitalize()
                args[key] = v
        return args
    
    @staticmethod
    def extract_request_by_content_type(request, default_accept='json', default_content='json'):
#        logger.exception('****************************')
#        logger.exception(request)
        args = {}
        try:
            _, content = RequestHeaderUtils.get_accept_content_type(request, 
                                                                    default_accept=default_accept, 
                                                                    default_content=default_content) 
#            logger.exception('requestxxxxxxxxxxxxxxxx')
#            logger.exception(content)
#            logger.exception(request.raw_post_data)
            #content_length = int(request.META.get('CONTENT_LENGTH', 0) if request.META.get('CONTENT_LENGTH') else 0)
            raw_post_data = request.raw_post_data.strip()
            if content == 'json':
                if raw_post_data:
                    args = simplejson.loads(raw_post_data)
            elif content == 'xml':
                if raw_post_data:
                    args = Xml2Json(raw_post_data).result
                    for (_, value) in args.iteritems():
                        args = value
            else:
                if raw_post_data:
                    str_raw = raw_post_data
                    key_values = str_raw.split('&')
                    for key_value in key_values:
                        kv = key_value.split('=')
                        args[kv[0]] = kv[1]
        except Exception, ex:
            logger.exception(ex)
            raise ParameterExtractFailed
        
        return args

    @staticmethod
    def convert_querydict_to_dict(querydict):
        return dict([(str(key), value) for key, value in querydict.iteritems()])
