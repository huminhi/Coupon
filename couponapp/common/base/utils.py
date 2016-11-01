'''
Created on Dec 26, 2011

@author: KhoaTran
'''
from xml.etree.ElementTree import fromstring
from django.conf import settings
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django_mysqlpool import auto_close_db
from lunex.common import log
from lunex.common.v2.utils.keyvalue import KeyValueUtils
from lunex.aaportal.common import CacheService
from lunex.aaportal.v2.crm.core.customer.ticket import UnreadTicketRepository
from lunex.aaportal.v2.crm.core.reseller.ticket import UnreadTicketRepository as UnreadTicketRepositoryReseller

logger = log.setup_logger('gui_base.utils')

class PermissionCacheUtils(object):
    CACHE_TIME_TO_EXPIRE = 60 * 60 * 1
    PERMISSION_CACHE_KEY = 'PERMISSION_CACHE_KEY'
    
    @staticmethod
    def get_cache_key(request,key):
        k = request.session.session_key;
        return ('%s_%s')%(k,key);
    
    @staticmethod
    def add_to_cache(req):
        CacheService.add_if_not_exists([
                                        CacheService.CacheObject(PermissionCacheUtils.get_cache_key(req,req.user.username),
                                                                 lambda arg:PermissionCacheUtils.load_permision_list(req.user),
                                                                 arg=None, 
                                                                 expire=PermissionCacheUtils.CACHE_TIME_TO_EXPIRE),        
                                        ]);
    
    @staticmethod
    @auto_close_db
    def load_permision_list(user):
        logger.debug('load_permision_list for user=%s' % user.username)
        return user.get_all_permissions()

class MenuUtils(object):
    @staticmethod
    def load_menu(req, user, menu_path=''):
        path = '/config/xml/menu_cfg.xml'
        if menu_path:
            path = menu_path
        f = open(settings.META_CONFIG_PATH + path)
        content = f.read()
        
        xml_document = fromstring(content)
        #xml_root = xml_document.find('.//Menu')
        arr = []
        
        CacheService.initalize_cache_for_session(req, PermissionCacheUtils.PERMISSION_CACHE_KEY, PermissionCacheUtils.add_to_cache);
        cache_key = PermissionCacheUtils.get_cache_key(req, user.username)
        CacheService.updateData(cache_key, user, False)
        user_permissions = user.get_all_permissions() #CacheService.get(cache_key)
        
        for xml_node in xml_document:
            try:
                menu_item = MenuUtils.__load_inner_menu(req, user, user_permissions, xml_node)
                if len(menu_item['items']) == 0:
                    menu_item['hidden'] = True 
                arr.append(menu_item)
                
            except Exception, ex:
                logger.exception(ex)
        f.close()
        
        return arr

    @staticmethod
    def __remove_hidden_items(arr):
        new_arr = []
        for mnui in arr:
            if mnui.get('hidden'):
                continue
            else:
                new_arr.append(mnui)
        return new_arr

    @staticmethod
    def __load_inner_menu(req, user, user_permissions, xml_menu_item):
        arr = []
        menu_item_dict = {}
        menu_item_dict['name'] = xml_menu_item.attrib.get('Name', '')
        menu_name = menu_item_dict['name']
        if menu_name == '-':
            menu_item_dict['separator'] = True
            menu_item_dict['name'] = ''
        if len(menu_name) > 1 and menu_name[0] == '-' and menu_name[-1] == '-':
            menu_item_dict['header'] = True
            menu_item_dict['name'] = menu_name[1:-1]
        
        url_name = xml_menu_item.attrib.get('UrlName', '')
        menu_item_dict['url'] = reverse(url_name) if url_name else '#'
        tmp_url = xml_menu_item.attrib.get('Url', '')
        tmp_url = MenuUtils.__replace_placeholder(user, tmp_url)
        menu_item_dict['url'] = tmp_url if tmp_url else menu_item_dict['url']
        perm = xml_menu_item.attrib.get('Permission', '')
        menu_item_dict['permission'] = perm if perm else ''
        menu_item_dict['has_permission'] = ((perm in user_permissions) or user.is_superuser) if perm else True
        
        for xml_sub_menu_item in xml_menu_item:
            try:
                arr.append(MenuUtils.__load_inner_menu(req, user, user_permissions, xml_sub_menu_item))
            except Exception, ex:
                logger.exception(ex)
        
        before_remove_count = len(arr)
        arr = MenuUtils.__remove_hidden_items(arr)
        
        #Separator and header processing
        if len(arr) > 0:
            for i in range(1, len(arr)):
                if arr[i-1].get('separator') and arr[i].get('separator'):
                    arr[i]['hidden'] = True
                if arr[i-1].get('header') and arr[i].get('separator'):
                    arr[i]['hidden'] = True
                if arr[i-1].get('separator') and arr[i].get('header'):
                    arr[i]['hidden'] = True
                if arr[i-1].get('header') and arr[i].get('header'):
                    arr[i]['hidden'] = True
        if len(arr) > 0 and (arr[-1].get('header') or arr[-1].get('separator')):
            arr[-1]['hidden'] = True
        
        arr = MenuUtils.__remove_hidden_items(arr)
        
        if len(arr) > 0:
            for i in range(1, len(arr)):
                if ((arr[i-1].get('separator') or arr[i-1].get('header')) 
                    and (arr[i].get('separator') or arr[i].get('header'))):
                    arr[i-1]['hidden'] = True
        arr = MenuUtils.__remove_hidden_items(arr)
        
        if len(arr) > 0 and (arr[0].get('header') or arr[0].get('separator')):
            #TODO: ask aKhoa to check again
            #arr[0]['hidden'] = True
            pass
        if len(arr) > 0 and (arr[-1].get('header') or arr[-1].get('separator')):
            arr[-1]['hidden'] = True
        arr = MenuUtils.__remove_hidden_items(arr)  
        #End Separator processing
                
        menu_item_dict['items'] = arr
        hidden = xml_menu_item.attrib.get('Hidden', False)
        try:
            hidden = bool(int(hidden))
        except:
            pass
        menu_item_dict['hidden'] = (hidden or not menu_item_dict['has_permission'] or (len(arr) == 0 and before_remove_count > 0))
        
        if len(arr) > 0 and not menu_item_dict['hidden']:
            perm_tmp = arr[0]['has_permission']
            hidden_tmp = arr[0]['hidden']
            if len(arr) > 1:
                for item in arr[1:]:
                    perm_tmp |= item['has_permission']
                    hidden_tmp &= item['hidden']
            
            menu_item_dict['hidden'] = (hidden_tmp or not perm_tmp)
        
        return menu_item_dict
    
    @staticmethod
    def __replace_placeholder(user, url, **kwargs):
        new_url = url.replace('__username__', user.username)
        return new_url

class JqGridUtils(object):
    class PaginatorWrapper():
        paginator = None
        data = None
    
    @staticmethod
    def make_paging_query_set(query_set, id, columns = None, page_size = 20, page_index = 1):    
        """
        Set page_size to None to not use paginator 
        """     
        rows = [];
        cell = None;
        if page_size is not None:
            paginator = Paginator(query_set, page_size)
            obj_list = paginator.page(page_index).object_list;
            pages = paginator.num_pages
            records = paginator.count
        else:
            obj_list = query_set
            pages = 1
            records = len(query_set)
            
        if columns == None and len(obj_list) > 0:
            columns = [attr for attr in dir(obj_list[0]) if not attr.startswith('_') ]
        
        count = 0;
        for obj in obj_list:
            cell = [];
            for p in columns:
                cell.append(KeyValueUtils.get_value(obj, p)) 
                
            count = count + 1; 
            rows.append({
                "id" : (obj[id] if isinstance(obj, dict) else getattr(obj,id)) if id else count,
                "cell" : cell
            });
            
        return {
                "page": page_index,
                "total": pages,
                "records": records,
                "rows": rows
                };     
           
    @staticmethod
    def make_paging_with_paginator(paginator_wrapper, id, columns = None, page_index = 1): 
        """
        Set paginator to None to not use paginator 
        """ 
        rows = [];
        cell = None;
        
        paginator = paginator_wrapper.paginator
        objs = paginator_wrapper.data
        
        if paginator is not None:
            pages = paginator.num_pages
            records = paginator.count
        else:
            pages = 1
            records = len(objs)
        
        count = 0
        for obj in objs:        
            if columns == None:
                cell =  obj.values();          
            else:
                cell = [];
                for p in columns:
                    cell.append(KeyValueUtils.get_value(obj, p))
            
            count = count + 1; 
            rows.append({
                "id" : (obj[id] if isinstance(obj, dict) else getattr(obj,id)) if id else count,
                "cell" : cell
            });
            
        return {
                "page": page_index,
                "total": pages,
                "records": records,
                "rows": rows
                };

class NotificationUtils(object):
    @staticmethod
    def load_crm_ticket_customer(user):
        return UnreadTicketRepository.get_unread_ticket_qs(user.profile.Entity)   
     
    @staticmethod
    def load_crm_ticket_retailer(user):
        return UnreadTicketRepositoryReseller.get_unread_ticket_qs(user.profile.Entity)    