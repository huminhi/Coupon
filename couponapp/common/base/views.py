# from django.views.generic.base import TemplateResponseMixin, TemplateView
# from django.core.exceptions import ImproperlyConfigured
#
# class PdfResponseMixin(object):
#     '''
#     Used to render PDF page.
#     '''
#     template_name = None
#     data = {}
#
#     def render_to_response(self, context, **response_kwargs):
#         return self.get_pdf_response(self.get_pdf_data(context))
#
#     def get_pdf_response(self, content, **httpresponse_kwargs):
#         return http.HttpResponse(content,
#                                  mimetype='application/pdf')
#
#     def get_pdf_data(self, context):
#         if self.template_name is None:
#             raise ImproperlyConfigured('template_name')
#         content = render_pdf(self.get_template_name(),
#                              self.get_data(context))
#         return content
#
#     def get_data(self, context={}):
#         data = context.get('data')
#         if data:
#             self.data = data
#         return self.data
#
#     def get_template_name(self):
#         return self.template_name
#
# class JsonErrorResponseMixin(object):
#     '''
#     Used to render JSON data when AJAX request has error.
#     '''
#     data = {}
#     def render_to_response(self, context, **response_kwargs):
#         "Returns a JSON response"
#         return self.get_json_response(EncodingUtils.encode_json(self.data))
#
# class JqgridResponseMixin(JsonResponseMixin):
#     '''
#     Used to render JqGrid format JSON response.
#     '''
#     '''
#     Column name that grid use to make Id column.
#     '''
#     id_col_name = None
#     '''
#     Whether using pagination.
#     '''
#     is_paginated = True
#
#     def render_to_response(self, context, **response_kwargs):
#         "Returns a JSON response"
#         return self.get_json_response(self.get_jqgrid_data(context))
#
#     def get_jqgrid_data(self, context):
#         "Convert the context dictionary into a JSON object"
#
#         if context.get('method', 'get') in ['get', 'post']:
#             result = EncodingUtils.encode_json(self.get_grid_data(context), default=EncodingUtils.json_gui_encode)
#         else:
#             result = self.get_json_data(context)
#         return result
#
#     def get_grid_data(self, context):
#         page_size = int(self.request.GET.get('rows', 20))
#         page_index = int(self.request.GET.get('page', 1))
#
#         if context.get('method', 'get') == 'post':
#             page_size = int(self.request.POST.get('rows', 20))
#             page_index = int(self.request.POST.get('page', 1))
#
# #        if self.id_col_name is None:
# #            raise ImproperlyConfigured('id_col_name')
#
#         data = self.get_data(context)
#         paginator_wrapper = self.get_paginator_wrapper(data)
#
#         if paginator_wrapper:
#             result = JqGridUtils.make_paging_with_paginator(paginator_wrapper, self.id_col_name,
#                                                             self.get_formatters(), page_index)
#         else:
#             result = JqGridUtils.make_paging_query_set(data, self.id_col_name, self.get_formatters(),
#                                                        page_size if self.is_paginated else None, page_index)
#
#         if 'userdata' in context:
#             result['userdata'] = context['userdata']
#
#         return result
#
#     def get_paginator_wrapper(self, context):
#         #Implement this method to return JqGridUtils.PaginatorWrapper
#         return None
#
#     def get_data(self, context={}):
#         data = context.get('data')
#         if data:
#             self.data = data
#         return self.data
#
# class HtmlView(TemplateResponseMixin):
#
#     def do_work(self, request, httpmethod_func, *args, **kwargs):
#         try:
#             response = super(HtmlView, self).do_work(request, httpmethod_func, *args, **kwargs)
#         except http.Http404:
#             context = super(HtmlView, self).get_context_data(**kwargs)
#             self.template_name = '404.html'
#             response = TemplateResponseMixin.render_to_response(self, context)
#         except Exception, ex:
#             logger.exception(ex)
#             context = super(HtmlView, self).get_context_data(**kwargs)
#
#             etype, value, tb = sys.exc_info()
#             formatted_exception = str(ex) + '\r\n'
#             for item in format_exception(etype, value, tb):
#                 formatted_exception += item
#             context['exception'] = formatted_exception
#             logger.exception(ex)
#             self.template_name = '500.html'
#             response = TemplateResponseMixin.render_to_response(self, context)
#         return response
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super(HtmlView, self).get_context_data(**kwargs)
#         context['menu'] = MenuUtils.load_menu(self.request, self.request.user)
#         context['crm'] = {}
#         context['crm']['customer_tickets'] = NotificationUtils.load_crm_ticket_customer(self.request.user)
#         context['crm']['retailer_tickets'] = NotificationUtils.load_crm_ticket_retailer(self.request.user)
#         return context
#
# class MixView(CsvResponseMixin, JsonResponseMixin, XmlResponseMixin, PdfResponseMixin, AuthenticatedView):
#
#     def render_to_response(self, context, **response_kwargs):
#         # Look for a 'f=json' GET argument
#         f = self.request.GET.get('f','json').lower()
#
#         if f == 'json':
#             return JsonResponseMixin.render_to_response(self, context)
#         elif f == 'xml':
#             return XmlResponseMixin.render_to_response(self, context)
#         elif f == 'csv':
#             return CsvResponseMixin.render_to_response(self, context)
#         elif f == 'pdf':
#             return PdfResponseMixin.render_to_response(self, context)
#         else:
#             raise UnsupportResponseFormat()
#
# class AjaxView(JsonResponseMixin, JsonErrorResponseMixin, AuthenticatedView):
#     '''
#     A view is used to work with AJAX and returns JSON response.
#     '''
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated():
#             return super(AuthenticatedView, self).dispatch(request, *args, **kwargs)
#         else:
#             self.data = {'ErrorCode': -403,
#                          'HasError': True,
#                          'Message': 'Session is out of date.'}
#
#             context = AuthenticatedView.get_context_data(self)
#             response = JsonErrorResponseMixin.render_to_response(self, context)
#             return response
#
#     def do_work(self, request, httpmethod_func, *args, **kwargs):
#         try:
#             response = AuthenticatedView.do_work(self, request, httpmethod_func, *args, **kwargs)
#         except Exception, ex:
#             logger.error('AjaxView Exception="%s" Data=%s' % (str(ex), str(self.data)[:255]))
#             logger.exception(ex)
#             #Overwrite data to get Error Response
#             self.data = {'ErrorCode': -1,
#                          'HasError': True,
#                          'Message': str(ex)}
#
#             context = AuthenticatedView.get_context_data(self)
#             f = self.request.GET.get('f','json').lower()
#             if f == 'csv':
#                 response = self.render_to_response(context)
#             else:
#                 response = JsonErrorResponseMixin.render_to_response(self, context)
#
#         return response
#
# class RawAjaxView(AuthenticatedView):
#     '''
#     A view is used to work with AJAX.
#     '''
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated():
#             return super(AuthenticatedView, self).dispatch(request, *args, **kwargs)
#         else:
#             return http.HttpResponseForbidden()
#
#     def render_to_response(self, context):
#         return http.HttpResponse(context['data'])
#
# class JqGridView(CsvResponseMixin, JqgridResponseMixin, HtmlResponseMixin, AjaxView):
#     '''
#     A view to render jqGrid.
#     '''
#     def render_to_response(self, context, **response_kwargs):
#         if context.get('method', 'get') in ['get', 'post']:
#             f = self.__get_format()
#             if f == 'csv':
#                 return self.render_to_csv(context)
#             if f == 'html':
#                 return self.render_to_html(context)
#             else:
#                 return self.render_to_grid(context)
#         else:
#             return JsonResponseMixin.render_to_response(self, context)
#
#     def get_context_data(self, **kwargs):
#         context = super(JqGridView, self).get_context_data(**kwargs)
#         context['grid_headers'] = self.headers
#         context['excluded_column_indexes'] = self.__get_exclude_column_indexes()
#         return context
#
#     def render_to_csv(self, context):
#         return CsvResponseMixin.render_to_response(self, context)
#
#     def render_to_html(self, context):
#         return HtmlResponseMixin.render_to_response(self, context)
#
#     def render_to_grid(self, context):
#         return JqgridResponseMixin.render_to_response(self, context)
#
#     def __get_format(self):
#         return self.request.GET.get('f','json').lower()
#
#     def __get_exclude_column_indexes(self):
#         return self.request.GET.get('exclcols','').lower().split('|')
#
# class HomepageView(HtmlView):
#     template_name = 'v2/ats/index.html'
#
# class AjaxHandleView(AjaxView):
#     handlers = {}
#
#     def do_get(self, request, **kwargs):
#         return self.__do_inner(request, **kwargs);
#
#     def do_post(self, request, **kwargs):
#         return self.__do_inner(request, **kwargs);
#
#     def get_handlers(self):
#         return self.handlers
#
#     def __do_inner(self, request, **kwargs):
#         handlers = self.get_handlers()
#         action = kwargs.get('action')
#         if action:
#             handler = handlers.get(action)
#             if handler:
#                 return handler(request)
#
#         raise AjaxHandlerNotFound('Not found [%s] action to do AJAX.' % action)
#
# class RawAjaxHandleView(RawAjaxView):
#     handlers = {}
#
#     def do_get(self, request, **kwargs):
#         return self.__do_inner(request, **kwargs);
#
#     def do_post(self, request, **kwargs):
#         return self.__do_inner(request, **kwargs);
#
#     def get_handlers(self):
#         return self.handlers
#
#     def __do_inner(self, request, **kwargs):
#         handlers = self.get_handlers()
#         action = kwargs.get('action')
#         if action:
#             handler = handlers.get(action)
#             if handler:
#                 return handler(request)
#
#         raise AjaxHandlerNotFound('Not found [%s] action to do AJAX.' % action)