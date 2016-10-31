'''
Created on Jan 17, 2012

@author: KhoaKhoi
'''
from lunex.common import log
from lunex.common.v2.base.exceptions import ParameterExtractFailed
from lunex.common.v2.utils.converters import Xml2Json

logger = log.setup_logger('common.v2.utils.request_utils')

class RequestHeaderUtils(object):
    @staticmethod
    def get_accept_content_type(request, default_accept='json', default_content='json'): 
        accept, content = default_accept, default_content
        accept_type = request.get_header('accept', '').lower()
        content_type = request.content_type.lower()
        
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
        for k, v in request.headers.iteritems():
            args[k] = v
        return args
    
    @staticmethod
    def extract_request_by_content_type(request, default_accept='json', default_content='json'):
        args = {}
        try:
            _, content = RequestHeaderUtils.get_accept_content_type(request, 
                                                                    default_accept=default_accept, 
                                                                    default_content=default_content) 
            content_length = int(request.content_length)
            if content == 'json':
                if content_length > 0:
                    args = request.json
            elif content == 'xml':
                if content_length > 0:
                    args = Xml2Json(request.body.getvalue()).result
                    for (_, value) in args.iteritems():
                        args = value
            else:
                if request.params:
                    for (key, value) in request.params.iteritems():
                        args[key] = value
        except Exception, ex:
            logger.exception(ex)
            raise ParameterExtractFailed
        
        return args

    @staticmethod
    def convert_querydict_to_dict(querydict):
        return dict([(str(key), value) for key, value in querydict.iteritems()])
