'''
Created on Jan 17, 2012

@author: KhoaTran
'''

from django.http import HttpResponse

class XmlResponse(HttpResponse):
    """\
    Return a HttpResponse with the Xml mimetype.
    If xml_clean is True, escape special characters in the string, and format it cleanly."""
    def __init__(self, content, xml_clean=False, status=200, **kwargs): 
        if xml_clean:
            from lxml.etree import tostring, fromstring, XMLSyntaxError
            try:
                content = tostring(fromstring(content), pretty_print=True)
            except XMLSyntaxError:
                pass # dont format anything ...
        super(XmlResponse, self).__init__(content, 
                                          mimetype='text/xml',
                                          content_type = 'application/xml; charset=utf-8', 
                                          status=status,
                                          **kwargs)