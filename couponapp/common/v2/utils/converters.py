'''
Created on Jan 17, 2012

@author: KhoaTran
'''
import decimal
import datetime
import simplejson
from xml.sax.saxutils import escape
from xml.parsers.expat import ParserCreate
from lunex.common.v2.utils.datetimes import DateTimeUtils
from lunex.common.v2.utils.numbers import NumberUtils, PrettyFloat
from lunex.common.v2.utils.strings import StringUtils

class Xml2Json:
    ## {{{ http://code.activestate.com/recipes/577494/ (r2)
    LIST_TAGS = ['COMMANDS']
    
    def __init__(self, data = None):
        self._parser = ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.result = None
        if data:
            self.feed(data)
            self.close()
        
    def feed(self, data):
        self._stack = []
        self._data = ''
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start(self, tag, attrs):
        #assert attrs == {}
        assert self._data.strip() == ''
        #print "START", repr(tag)
        self._stack.append([tag])
        self._data = ''

    def end(self, tag):
        #print "END", repr(tag)
        last_tag = self._stack.pop()
        assert last_tag[0] == tag
        if len(last_tag) == 1: #leaf
            data = self._data
        else:
            if tag not in Xml2Json.LIST_TAGS:
                # build a dict, repeating pairs get pushed into lists
                data = {}
                for k, v in last_tag[1:]:
                    if k not in data:
                        data[k] = v
                    else:
                        el = data[k]
                        if type(el) is not list:
                            data[k] = [el, v]
                        else:
                            el.append(v)
            else: #force into a list
                data = [{k:v} for k, v in last_tag[1:]]
        if self._stack:
            self._stack[-1].append((tag, data))
        else:
            self.result = {tag:data}
        self._data = ''

    def data(self, data):
        self._data = data

class Dict2Xml:
    def __init__(self, d, xml = ''):
        self.result = self.convert(d, xml)
    
    def convert(self, d, xml = ''):
        ## {{{ http://code.activestate.com/recipes/576939/ (r1)
        for key,value in d.iteritems():
            str_value = value
            if type(value) in [str, unicode, int, float, bool, long, decimal.Decimal]:
                str_value = escape(str(value))
                value = escape(str(value))
            elif type(value) in [datetime.datetime,]:
                str_value = value.isoformat()
                value = value.isoformat()
            elif type(value) in [list, tuple]:
                item_xml = ''
                for item in value:
                    if type(item) in [unicode, int, float, bool, long, decimal.Decimal]:
                        item = escape(str(item))
                    elif type(item) in [list, tuple]:
                        item = {key: item}
                        
                    exec 'content = '+ {'str': 'item', 'dict': 'self.convert(item)'}[type(item).__name__]
                    item_xml += '<%s>%s</%s>' % ('Item', str(content), 'Item')
                str_value = str(item_xml)
                value = str(item_xml)
            elif value is None:
                str_value = ''
            elif type(value) not in [str, dict]:
                str_value = str(value)
                
            exec 'content = '+ {'str': 'value', 'dict': 'self.convert(value)'}[type(str_value).__name__]
            xml += '<%s>%s</%s>' % (key, str(content), key)
        return xml

class EncodingUtils(object):
    @staticmethod
    def encode_json(val, default=None):
        if default:
            return simplejson.dumps(val, default=default, sort_keys=True)
        return simplejson.dumps(val, default=EncodingUtils.__json_default_encode, sort_keys=True)
    
    @staticmethod
    def __json_default_encode(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            #return NumberUtils.format_currency(obj)
            return PrettyFloat(str(obj))
        
        return str(obj)
    
    @staticmethod
    def json_gui_encode(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%m/%d/%Y %H:%M:%S')
        if isinstance(obj, decimal.Decimal):
            return NumberUtils.format_currency(obj)
        
        return str(obj)