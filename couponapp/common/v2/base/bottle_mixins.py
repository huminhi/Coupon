'''
Created on Jun 24, 2013

@author: KhoaTran
'''

import bottle
from lunex.common.v2.base.mixins import JsonResponseMixin, XmlResponseMixin

class BottleJsonResponseMixin(JsonResponseMixin):
    def get_json_response(self, content, **httpresponse_kwargs):
        'Bottle auto care about json'
        bottle.response.content_type = 'application/json'
        return content
        
class BottleXmlResponseMixin(XmlResponseMixin):
    def get_xml_response(self, content, **httpresponse_kwargs):
        bottle.response.content_type = 'text/xml'
        content = '<{root}>{content}</{root}>'.format(root=self.get_root(),
                                                      content=content)
        if httpresponse_kwargs.get('xml_clean') == True:
            from lxml.etree import tostring, fromstring, XMLSyntaxError
            try:
                content = tostring(fromstring(content), pretty_print=True)
            except XMLSyntaxError:
                pass # dont format anything ...
            
        return content
        