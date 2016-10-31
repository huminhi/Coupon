

__all__ = [
        'ModelViews',
        ]


import math

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from lunex.common.resp import JsonResponse


class ModelViews(object):
    list_view_template = None
    selection_op_template = None
    error_template = None

    default_sort_order = None
    list_key = None
    model_name = None

    def __init__(self, req):
        self.req = req
        self.get = req.GET
        self.post = req.POST
        self.user = req.user
        self.profile = self.user.get_profile()

    ###########
    ## Views ##
    ###########

    def list_view(self, params=None, **kws):
        form = self.get_search_form()
        if not params:
            params = {}
        params = dict(params, profile=self.profile, form=form)
        params.update(kws)
        lvp = self.get_list_view_params()
        if lvp:
            params.update(lvp)
        return render_to_response(self.list_view_template, params,
                context_instance=RequestContext(self.req))

    def list_json(self):
        objects = self.objects
        objects = self.search_form_filter(objects)
        objects = self.search_form_order(objects)
        paging = self.search_form_paging(objects)
        objects = self.search_form_slice(objects, paging)
        data = [
                { 'id': obj.pk, 'cell': self.object_vec(obj), }
                for obj in objects.all()
                ]
        return JsonResponse(dict(paging, rows=data))

    def detail(self, object_id):
        raise NotImplementedError

    ###########
    ## Forms ##
    ###########

    def get_search_form(self, *args, **kwarg):
        raise NotImplementedError

    def get_form(self, *args, **kwargs):
        raise NotImplementedError

    def search_form_filter(self, objects):
        return objects

    def search_form_order(self, objects):
        sidx = self.get.get('sidx', self.default_sort_order)
        if sidx:
            objects = objects.order_by(sidx)
        if self.get.get('sord') == 'desc':
            objects = objects.reverse()
        return objects

    def search_form_paging(self, objects):
        page = int(self.get.get('page', '1'))
        pagelen = int(self.get.get('pagelen', '50'))
        records = objects.count()
        total_pages = ( math.ceil(records/float(pagelen)) if records > 0 else 0 )
        if page > total_pages:
            page = total_pages
        paging = {
                'total': total_pages,
                'page': page,
                'records': records,
                }
        return paging

    def search_form_slice(self, objects, paging):
        pagelen = int(self.get.get('pagelen', '50'))
        start = pagelen * (paging['page'] - 1)
        if start < 0:
            start = 0
        objects = objects[start:start+pagelen]
        return objects

    #########################
    ## Template Parameters ##
    #########################

    def get_list_view_params(self):
        return None

    ##################
    ## List Actions ##
    ##################

    def list_action(self, name, action):
        pks = [
                self.safe_int(pk)
                for pk in self.get.getlist(self.list_key)
                if pk
                ]
        if not pks:
            return bad_request(req, 'Invalid request', 'You must provide a list of primary keys')
        objects = self.objects.in_bulk(pks).values()
        i = 0
        errors = []
        for obj in objects:
            try:
                action(obj)
            except Exception, e:
                errors += ( 'ERROR on %s: %s' % (unicode(obj), arg) for arg in e.args )
            i += 1
        params = {
                'op': name,
                'name': self.model_name,
                'objects': objects,
                'errors': errors,
                }
        return render_to_response(self.selection_op_template, params,
                context_instance=RequestContext(self.req))

    #################################
    ## Object Access and Filtering ##
    #################################

    def get_objects(self):
        return ()
    @property
    def objects(self):
        try:
            objects = self.__objects
        except AttributeError:
            objects = self.__objects = self.get_objects()
        return objects

    def object_vec(self, obj):
        return ()

    def _filter(self, objects, key, op, params=None):
        if params is None:
            params = self.get
        value = params.get(key)
        if value is not None:
            filters = { key+'__'+op: value }
            objects = objects.filter(**filters)
        return objects

    def __fdr(self, objects, params, key, suffix, op):
        ff = key + suffix
        value = params.get(ff)
        if value is not None:
            filter = { key+'__'+op: value }
            objects = objects.filter(**filter)
        return objects

    def _filter_date_range(self, objects, key, from_suffix='_from', to_suffix='_to', params=None):
        if params is None:
            params = self.get
        objects = self.__fdr(objects, params, key, from_suffix, 'gte')
        objects = self.__fdr(objects, params, key, to_suffix, 'lte')
        return objects

    def _filter_yesno(self, objects, key, params=None):
        if params is None:
            params = self.get
        value = params.get(key)
        if value is None:
            return objects
        value = int(value)
        if value == 2:
            filters = { key: True }
            return objects.filter(**filters)
        elif value == 3:
            filters = { key: False }
            return objects.filter(**filters)
        else:
            return objects

    _filter_range = _filter_date_range

    ###############
    ## Utilities ##
    ###############

    @staticmethod
    def safe_date_str(date):
        if date is None:
            return u''
        else:
            return unicode(date.isoformat())

    @staticmethod
    def safe_int(data):
        try:
            return int(data)
        except:
            return data

