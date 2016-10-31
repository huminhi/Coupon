

__all__ = [
        'get_xml_attr',
        'xml_indent',
        'XmlWriter',
        ]


from contextlib import contextmanager
import os
import re
from xml.etree import cElementTree as ET
from xml.sax.saxutils import XMLGenerator


NL = unicode(os.linesep)


def get_xml_attr(text):
    """\
    Return a dictionary of parameters parsed from the XML like string.
    
    >>> get_xml_attr('<session name="foo" value="bar" code="baz">') 
    { 'name': 'foo', 'value': 'bar', 'code': 'baz' }

    """
    return dict(re.findall('(\w+)=\"(\w+)\"', text))


def xml_indent(elem, indent='  ', level=0):
    """ This indents the structure of an ElementTree. """
    i = '\n' + (indent * level)
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        for e in elem:
            xml_indent(e, level=level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + indent
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    return elem


class XmlWriter(object):

    def __init__(self, f, indent=False, tab=u'  '):
        self.f = f
        self.indent = indent
        self.tab = tab
        self.level = 0
        self.xmlgen = XMLGenerator(f, 'UTF-8')

    @contextmanager
    def doc(self):
        self.xmlgen.startDocument()
        try:
            yield
        finally:
            self.xmlgen.endDocument()

    @contextmanager
    def tag(self, name, attrs=None, **kws):
        attrs = self.merge_attrs(attrs, kws)
        if self.indent:
            if self.level:
                self.xmlgen.characters(NL)
            self.xmlgen.characters(self.tab * self.level)
            self.level += 1
        self.xmlgen.startElement(name, attrs)
        try:
            yield
        finally:
            self.level -= 1
            if self.indent:
                self.xmlgen.characters(NL)
                self.xmlgen.characters(self.tab * self.level)
            self.xmlgen.endElement(name)

    @contextmanager
    def nstag(self, name, qname, attrs=None, **kws):
        attrs = self.merge_attrs(attrs, kws)
        if self.indent:
            if self.level:
                self.xmlgen.characters(NL)
            self.xmlgen.characters(self.tab * self.level)
            self.level += 1
        self.xmlgen.startElementNS(name, qname, attrs)
        try:
            yield
        finally:
            self.level -= 1
            if self.indent:
                self.xmlgen.characters(NL)
                self.xmlgen.characters(self.tab * self.level)
            self.xmlgen.endElementNS(name, qname)

    @contextmanager
    def prefixmap(self, prefix, uri):
        self.xmlgen.startPrefixMapping(prefix, uri)
        try:
            yield
        finally:
            self.xmlgen.endPrefixMapping(prefix)

    def texttag(self, name, content, attrs=None, **kws):
        attrs = self.merge_attrs(attrs, kws)
        if self.indent:
            if self.level:
                self.xmlgen.characters(NL)
            self.xmlgen.characters(self.tab * self.level)
        self.xmlgen.startElement(name, attrs)
        if isinstance(content, str):
            self.xmlgen.characters(unicode(content, 'utf-8', 'replace'))
        elif isinstance(content, unicode):
            self.xmlgen.characters(content)
        else:
            self.xmlgen.characters(unicode(content))
        self.xmlgen.endElement(name)

    def emptytag(self, name, attrs=None, **kws):
        attrs = self.merge_attrs(attrs, kws)
        if self.indent:
            self.xmlgen.characters(NL)
            self.xmlgen.characters(self.tab * self.level)
        self.xmlgen.startElement(name, attrs)
        self.xmlgen.endElement(name)

    def merge_attrs(self, attrs, kws):
        attrs = (dict(attrs) if attrs is not None else {})
        attrs.update(kws)
        return attrs

    def element(self, elem):
        """\
        This inserts an ElementTree into this stream.

        If indent is set, this modifies the input tree.

        """

        if self.indent:
            self.f.write(self.tab*(self.level+1))
            xml_indent(elem, self.tab, self.level+1)
        self.f.write(ET.tostring(elem))
        self.f.write(NL)


