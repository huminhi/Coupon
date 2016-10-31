'''
Created on Jan 17, 2012

@author: KhoaTran
'''
import StringIO
import csv
from django.http import HttpResponse
from lunex.common import log
from lunex.common.v2.utils.strings import StringUtils
from lunex.common.v2.utils.converters import EncodingUtils, Dict2Xml
from lunex.common.resp import XmlResponse
from lunex.common.v2.utils.keyvalue import KeyValueUtils
from django.template.loader import get_template
from django.template.context import RequestContext, Context

logger = log.setup_logger('common.v2.base.mixins')

class CsvResponseMixin(object):
    '''
    Used to render CSV file.
    '''
    #Download file name
    filename = 'Untitled.csv'
    #Data to render CSV, could be a queryset
    data = [] 
    #Header of CSV
    headers = []
    #footer
    footer = []
    #Data column of CSV
    formatters = []
    #Delimiter of CSV. Default is ','
    delimiter = ','
    #Extra header of CSV
    extra = []
    #Excluded column indexes
    excluded_column_indexes = []
    
    def render_to_response(self, context, **response_kwargs):
        "Returns a CSV response."
        return self.get_csv_response(self.get_csv_data(context))
    
    def get_csv_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        response = HttpResponse(content,
                                mimetype='application/ms-excel',
                                **httpresponse_kwargs)
        response['Content-Disposition'] = 'attachment; filename=%s' % self.get_filename();
        return response
        
    def get_csv_data(self, context):
        out = StringIO.StringIO()
        writer = csv.writer(out, delimiter=self.delimiter)
        
        objs = self.get_data(context)
        #In case there is error
        if type(objs) is dict:
            if objs.get('ErrorCode', -1) < 0:
                writer.writerow(CsvResponseMixin.__format_csv_row(['ErrorCode', objs.get('ErrorCode', -1)]))
                writer.writerow(CsvResponseMixin.__format_csv_row(['Message', objs.get('Message','')]))
                return out.getvalue()
        
        extra = self.get_extra()
        formatters = self.get_formatters()
        for info in extra:
            cell = []
            cell.append(info['Name'])
            cell.append(info['Value'])
            writer.writerow(CsvResponseMixin.__format_csv_row(cell))
        
        exclcols = self.get_excluded_column_indexes(context)
        header = self.get_headers()
        tmp_header = []
        for i in range(len(header)):
            if str(i) in exclcols:
                pass
            elif not header[i]:   #header = ""
                pass
            else:
                tmp_header.append(header[i])
        writer.writerow(tmp_header)
        
        for obj in objs:
            cell = [];
            i = 0
            for p in formatters[:len(header)]: #just get enought data for header
                if str(i) in exclcols:
                    pass
                elif not header[i]:
                    pass
                else:
                    cell.append(KeyValueUtils.get_value(obj, p))
                i += 1
            try:
                writer.writerow(CsvResponseMixin.__format_csv_row(cell))
            except:
                pass
            
        
        # Add footer 
        obj = self.get_footer(context);
        cell = [];
        i = 0
        for p in formatters[:len(header)]: #just get enough data for header
            if str(i) in self.excluded_column_indexes:
                pass
            elif not header[i]:
                pass
            else:
                try:
                    value = KeyValueUtils.get_value(obj, p)
                    if value != '$0.00' and value != 0 and value != '#N/A':
                        cell.append(value)
                    else:
                        cell.append("")
                except:
                    cell.append("")
                    pass
            i += 1
        try:
            writer.writerow(CsvResponseMixin.__format_csv_row(cell))
        except:
            pass
            
        return out.getvalue()

    def get_filename(self):
        return self.filename
    
    def get_data(self, context={}):
        data = context.get('data')
        if data != None:
            self.data = data 
        return self.data

    def get_footer(self, context={}):
        footer = context.get('userdata');
        if footer != None:
            self.footer = footer
        return self.footer
    
    def get_excluded_column_indexes(self, context={}):
        excluded_column_indexes = context.get('excluded_column_indexes')
        if excluded_column_indexes != None:
            self.excluded_column_indexes = excluded_column_indexes 
        return self.excluded_column_indexes
    
    def get_delimiter(self):
        return self.delimiter
    
    def get_headers(self):
        return self.headers
    
    def get_formatters(self):
        return self.formatters
    
    def get_extra(self):
        return self.extra
    
    @staticmethod
    def __format_csv_row(row):
        for i in range(0,len(row)):
            row[i] = StringUtils.remove_nonascii_chars(row[i]);
        return row;

class HtmlResponseMixin(object):
    '''
    Used to render Html file.
    '''
    #Download file name
    html_template_name = 'Untitled.html'
    #title of print page
    title = ''
    #Data to render Html, could be a queryset
    data = [] 
    #Header of Html
    headers = []
    #footer
    footer = []
    #Data column of Html
    formatters = []
    #Extra header of Html
    extra = []
    #Excluded column indexes
    excluded_column_indexes = []
    
    def render_to_response(self, context, **response_kwargs):
        "Returns a Html response."
        return self.get_html_response(self.get_html_data(context))
    
    def get_html_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        response = HttpResponse(content,
                                mimetype='text/html',
                                **httpresponse_kwargs)
        return response
        
    def get_html_data(self, context):
        template = get_template(self.html_template_name)
        exclcols = self.get_excluded_column_indexes(context)
        
        formatters = self.get_formatters()
        header = self.get_headers()
        tmp_header = []
        for i in range(len(header)):
            if str(i) in exclcols:
                pass
            elif not header[i]:   #header = ""
                pass
            else:
                tmp_header.append(header[i])
        
        objs = self.get_data(context)
        tmp_data = []
        for obj in objs:
            cell = [];
            i = 0
            for p in formatters[:len(header)]: #just get enought data for header
                if str(i) in exclcols:
                    pass
                elif not header[i]:
                    pass
                else:
                    cell.append(KeyValueUtils.get_value(obj, p))
                i += 1
            tmp_data.append(cell)
            
        
        #Add Footer
        obj = self.get_footer(context)
        cell = []
        i = 0;
        for p in formatters[:len(header)]: #just get enought data for header
            if str(i) in exclcols:
                pass
            elif not header[i]:
                pass
            else:
                try:
                    value = KeyValueUtils.get_value(obj, p)
                    if value != '$0.00' and value != 0 and value != '#N/A':
                        cell.append(value)
                    else:
                        cell.append("")
                except:
                    cell.append("")
                    pass
            i += 1
        tmp_data.append(cell)
        
        html = template.render(Context({'header': tmp_header, 'data': tmp_data, 'title': self.get_title()}))
        return html
    
    def get_excluded_column_indexes(self, context={}):
        excluded_column_indexes = context.get('excluded_column_indexes')
        if excluded_column_indexes != None:
            self.excluded_column_indexes = excluded_column_indexes 
        return self.excluded_column_indexes
    
    def get_data(self, context={}):
        data = context.get('data')
        if data != None:
            self.data = data 
        return self.data
    
    def get_title(self, context={}):
        return self.title
    
    def get_footer(self, context={}):
        footer = context.get('userdata');
        if footer != None:
            self.footer = footer
        return self.footer

    def get_headers(self):
        return self.headers
    
    def get_formatters(self):
        return self.formatters
    
    def get_extra(self):
        return self.extra
   
class JsonResponseMixin(object):
    '''
    Used to render JSON response.
    '''
    data = {}
    def render_to_response(self, context, **response_kwargs):
        "Returns a JSON response"
        return self.get_json_response(self.get_json_data(context), **response_kwargs)
    
    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                            content_type='application/json; charset=utf-8',
                            **httpresponse_kwargs)
        
    def get_json_data(self, context):
        "Convert the context dictionary into a JSON object"
        return EncodingUtils.encode_json(self.get_data(context))

    def get_data(self, context={}):
        data = context.get('data')
        if data:
            self.data = data 
        return self.data
    
class XmlResponseMixin(object):
    '''
    Used to render XML response.
    '''
    data = {}
    '''
    Root of XML response.
    '''
    root = 'Response'
    
    def render_to_response(self, context, **response_kwargs):
        "Returns a XML response"
        return self.get_xml_response(self.get_xml_data(context), **response_kwargs)
    
    def get_xml_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return XmlResponse('<{root}>{content}</{root}>'.format(root=self.get_root(), 
                                                               content=content),
                           **httpresponse_kwargs)
        
    def get_xml_data(self, context):
        "Convert the context dictionary into a XML object"
        data = self.get_data(context)
        if type(data) is list:
            data = {'List': data}
        return Dict2Xml(data).result

    def get_data(self, context={}):
        data = context.get('data')
        if data:
            self.data = data 
        return self.data
    
    def get_root(self):
        return self.root
    