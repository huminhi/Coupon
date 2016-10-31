

__all__ = [
        'json_to_datetime',
        'TextResponse',
        'JsonResponse',
        'to_json_resp',
        'to_csv_resp',
        'bad_request',
        ]


import csv
from datetime import date, datetime

from django.core.serializers import json, serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader, RequestContext
from django.utils import simplejson


DT_FORMAT = u'%Y-%m-%dT%H:%M:%SZ'



def json_to_datetime(json_str, format=DT_FORMAT):
    """\
    This takes a string-date, formatted according to ISO something-or-other
    (like "2009-07-22T19:30:53Z") and returns a datetime object.

    If you need another format, you pass it to this functiont too.

    """

    return datetime.strptime(json_str, format)


class TextResponse(HttpResponse):
    """\
    Return a HttpResponse with the plaintext mimetype.
    If xml_clean is True, escape special characters in the string, and format it cleanly."""
    def __init__(self, content, xml_clean=False): 
        if xml_clean:
            from lxml.etree import tostring, fromstring, XMLSyntaxError
            try:
                content = tostring(fromstring(content), pretty_print=True)
            except XMLSyntaxError:
                pass # dont format anything ...
        super(TextResponse, self).__init__(content, mimetype='text/plain')
    
class XmlResponse(HttpResponse):
    """\
    Return a HttpResponse with the Xml mimetype.
    If xml_clean is True, escape special characters in the string, and format it cleanly."""
    def __init__(self, content, xml_clean=False, status=200): 
        if xml_clean:
            from lxml.etree import tostring, fromstring, XMLSyntaxError
            try:
                content = tostring(fromstring(content), pretty_print=True)
            except XMLSyntaxError:
                pass # dont format anything ...
        super(XmlResponse, self).__init__(content, mimetype='text/xml', status=status)

class JsonResponse(HttpResponse):
    """ From http://www.djangosnippets.org/snippets/154/ """
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = simplejson.dumps(
                    object, indent=2, cls=json.DjangoJSONEncoder,
                    ensure_ascii=False,
                    )
        super(JsonResponse, self).__init__(content, mimetype='application/json')


def to_json_resp(obj, resp=None):
    """ This serializes an object to an HttpResponse object as JSON. """
    resp = (resp
            if resp is not None
            else HttpResponse(mimetype='application/json'))
    simplejson.dump(obj, resp, cls=json.DjangoJSONEncoder)
    return resp


def to_csv_resp(obj, filename='data.csv', resp=None):
    """ Return a CSV file, with content disposition set to filename """
    resp = (resp
            if resp is not None
            else HttpResponse(mimetype='text/csv'))
    resp['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = csv.writer(resp)
    for row in obj:
        writer.writerow(row)
    return resp


# TODO add error logging in bad request
def bad_request(req, title, message, cls=HttpResponseBadRequest, tmpl='lunex/error_page.html'):
    t = loader.get_template(tmpl)
    c = RequestContext(req, {
        'error_title': title,
        'message': message,
        'http_referer': req.META.get('HTTP_REFERER'),
        })
    return cls(t.render(c))


