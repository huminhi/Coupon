'''
Created on Sep 6, 2011

@author: KhoaTran
'''

import uuid
from lunex.common import log
from lunex.common.v2 import services

logger = log.setup_logger('customer.services.pos.api') 

class PosService(services.ApiService):
    '''
    Point of Sale Service
    '''
    def __init__(self, entity_user, service_url=None, logger_func=None, **kwargs):
        if entity_user is None:
            raise services.InvalidEntityUser
        
        super(PosService, self).__init__(entity_user, service_url, logger_func, **kwargs)
        
    def get_account(self, sku, phone):
        '''
        Get customer account.
        - sku: SKU of phone that customer account registered
        - phone: Main registered phone of customer account
        '''
        url = 'PosService.svc/sellers/{0}/sku/{1}/phone/{2}'
        url = url.format(self.get_entity_user(), sku, phone)
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result['Account']
    
    def get_account_by_pin(self, pin):
        '''
        Get customer account by PIN.
        - pin: PIN of customer
        '''
        url = 'PosService.svc/sellers/{0}/pin/{1}'
        url = url.format(self.get_entity_user(), pin)
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result['Account']
    
    def get_account_by_pins(self, pins=[]):
        '''
        Get customer account by PIN.
        - pin: PIN of customer
        '''
        url = 'PosService.svc/sellers/{0}/pin/?pin={1}'
        url = url.format(self.get_entity_user(), '|'.join(pins))
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result
    
    def update_account(self, sku, phone, account_dict={}, notify=False, **kwargs):
        '''
        Update customer account, if it does not exist, create a new one.
        - sku: SKU of phone that customer account registered
        - phone: Main registered phone of customer account
        - notify: Notify by SMS to customer
        - kwargs['lang']: Language of main registered phone number
        - kwargs['phone_type']: Phone type of main registered phone number
        - kwargs['promo']: Promotion code
        - kwargs['new_cust_bonus']: New customer bonus
        - kwargs['ref_name']: Referral name
        - kwargs['ref_phone']: Referral phone
        '''
        lang = '&lang=' + kwargs.get('lang') if kwargs.get('lang') else ''
        type = '&phone_type=' + kwargs.get('phone_type') if kwargs.get('phone_type') else ''
        promo = '&promo=' + kwargs.get('promo') if kwargs.get('promo') else ''
        new_cust_bonus = '&newcustbonus=' + kwargs.get('new_cust_bonus') if kwargs.get('new_cust_bonus') else ''
        
        url = 'PosService.svc/sellers/{0}/sku/{1}/phone/{2}?passcode=&notify={3}&refname={4}&refphone={5}{6}{7}{8}{9}'
        url = url.format(self.get_entity_user(),
                         sku, phone, self.__get_notify(notify),
                         kwargs.get('ref_name', ''),
                         kwargs.get('ref_phone', ''),
                         lang, type, promo, new_cust_bonus)
        
        result = self.call_service(self.HTTP_PUT, url, params=account_dict)
        
        return result['Account']
    
    def update_account_original_retailer(self, sku, phone, retailer=''):
        url = 'PosService.svc/sellers/{0}/sku/{1}/phone/{2}'
        url = url.format(self.get_entity_user(), sku, phone)
        
        result = self.call_service(self.HTTP_PUT, url, params={'CreatedBy':retailer})
        
        return result['Account']
    
    def update_unlimited_status(self, pin, status, minutes=None, expired_date=None):
        if minutes is not None:
            minutes = ('&minutes=' + str(minutes)) if minutes is not None else ''
        else:
            minutes = ''
        if expired_date:
            expired_date = ('&expired_date=' + expired_date.strftime('%Y%m%d%H%M%S')) if expired_date else ''
        else:
            expired_date = ''
        url = 'PosService.svc/sellers/{0}/unlimited/{1}?status={2}{3}{4}'
        
        url = url.format(self.get_entity_user(),
                         pin,
                         status,
                         minutes,
                         expired_date)
        
        result = self.call_service(self.HTTP_PUT, url)
        return result
    
    def get_registered_phones(self, pin):
        '''
        Get a list of registered phone for an account.
        - pin: PIN of customer
        '''
        url = 'PosService.svc/sellers/{0}/pin/{1}/registerphone'
        url = url.format(self.get_entity_user(), pin)
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result['List']
    
    def get_registered_phone(self, pin, phone):
        '''
        Get a registered phone for an account.
        - pin: PIN of customer
        - phone: Phone number of customer
        '''
        url = 'PosService.svc/sellers/{0}/pin/{1}/registerphone/{2}'
        url = url.format(self.get_entity_user(), pin, phone)
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result['RegisterPhone']
    
    def update_registered_phone(self, pin, notify=False, **kwargs):
        '''
        Add/update a registered phone for an account.
        '''
        url = 'PosService.svc/sellers/{0}/pin/{1}/registerphone?notify={notify}'
        url = url.format(self.get_entity_user(), pin, 
                         notify=self.__get_notify(notify))
        result = self.call_service(self.HTTP_PUT, url, params=kwargs)
        
        return result['RegisterPhone']
        
    def delete_registered_phone(self, pin, reg_phone, notify=False):
        '''
        Delete a registered phone. If a main number is deleted, 
        the next one in the list will become main.
        '''
        url = 'PosService.svc/sellers/{0}/pin/{1}/registerphone/{2}?notify={notify}'
        url = url.format(self.get_entity_user(), pin, reg_phone,
                         notify=self.__get_notify(notify))
        
        self.call_service(self.HTTP_DELETE, url, params=None)
        
    def get_speed_dials(self, pin):
        '''
        Get a list of speed dials for an account.
        - pin: PIN of customer
        '''
        url = 'PosService.svc/sellers/{0}/pin/{1}/speeddial'
        url = url.format(self.get_entity_user(), pin)
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result['List']
    
    def get_speed_dial(self, pin, number):
        '''
        Get a speed dial for an account.
        - pin: PIN of customer
        - number: Speed dial number
        '''
        url = 'PosService.svc/sellers/{0}/pin/{1}/speeddial/{2}'
        url = url.format(self.get_entity_user(), pin, number)
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result['SpeedDial']
    
    def update_speed_dial(self, pin, notify=False, **kwargs):
        '''
        Add/update a speed dial for an account.
        '''
        url = 'PosService.svc/sellers/{0}/pin/{1}/speeddial?notify={notify}'
        url = url.format(self.get_entity_user(), pin, 
                         notify=self.__get_notify(notify))
        result = self.call_service(self.HTTP_PUT, url, params=kwargs)
        
        return result['SpeedDial']
        
    def delete_speed_dial(self, pin, number, notify=False):
        '''
        Delete a speed dial.
        '''
        url = 'PosService.svc/sellers/{0}/pin/{1}/speeddial/{2}?notify={notify}'
        url = url.format(self.get_entity_user(), pin, number,
                         notify=self.__get_notify(notify))
        
        self.call_service(self.HTTP_DELETE, url, params=None)
    
    def make_raw_order(self, sku, cid=None, notify=False, **kwargs):
        '''
        Make an order.
        - sku: SKU of order
        - cid: A unique number to avoid repeated order
        - notify: Notify by SMS to customer
        - kwargs['card_id']: Id of credit card
        - kwargs['phone']: Phone to refill
        - kwargs['topup_phone']: Phone to make Top-Up order
        - kwargs['topup_name']: 
        - kwargs['amount']: Order amount, default = 0
        - kwargs['quantity']: Quantity, default = 1
        - kwargs['phone_type']: Phone type of order, value = [cell, landline]
        - kwargs['lang']: Language of phone number, default = xx
        - kwargs['ref_name']: Referral name
        - kwargs['ref_phone']: Referral phone
        - kwargs['mrule']: Rule
        - kwargs['promo']: Promotion with order
        - kwargs['new_cust_bonus']: New customer bonus
        - kwargs['merchantname']
        - kwargs['merchantid']
        '''
        uuid_str = cid if cid else uuid.uuid1().__str__()
        
        card_id = ('&cardid=%s' % kwargs.get('card_id')) if kwargs.get('card_id') else ''
        phone = ('&phone=%s' % kwargs.get('phone')) if kwargs.get('phone') else ''
        topup_phone = ('&topup_phone=%s' % kwargs.get('topup_phone')) if kwargs.get('topup_phone') else ''
        topup_name = ('&topup_name=%s' % kwargs.get('topup_name')) if kwargs.get('topup_name') else ''
        amount = ('&amount=%s' % str(kwargs.get('amount'))) if kwargs.get('amount') else '&amount=0'
        quantity = ('&quantity=%s' % str(kwargs.get('quantity'))) if kwargs.get('quantity') else ''
        type = ('&phone_type=%s' % kwargs.get('phone_type')) if kwargs.get('phone_type') else ''
        lang = ('&lang=%s' % kwargs.get('lang')) if kwargs.get('lang') else ''
        ref_name = ('&refname=%s' % kwargs.get('ref_name')) if kwargs.get('ref_name') else ''
        ref_phone = ('&refphone=%s' % kwargs.get('ref_phone')) if kwargs.get('ref_phone') else ''
        mrule = ('&mrule=%s' % kwargs.get('mrule')) if kwargs.get('mrule') else ''
        promo = ('&promo=%s' % kwargs.get('promo')) if kwargs.get('promo') else ''
        new_cust_bonus = ('&newcustbonus=%s' % kwargs.get('new_cust_bonus')) if kwargs.get('new_cust_bonus') else ''
        merchantname = ('&merchantname=%s' % kwargs.get('merchantname')) if kwargs.get('merchantname') else ''
        merchantid = ('&merchantid=%s' % kwargs.get('merchantid')) if kwargs.get('merchantid') else ''
        
        url = 'PosService.svc/sellers/{0}/orders/{cid}/sku/{sku}?notify={notify}'
        url += '{card_id}{phone}{topup_phone}{topup_name}{amount}{quantity}{type}{lang}'
        url += '{ref_name}{ref_phone}{mrule}{promo}{new_cust_bonus}{merchantname}{merchantid}'
        url = url.format(self.get_entity_user(),
                         cid=uuid_str,
                         sku=sku, notify=self.__get_notify(notify),
                         card_id=card_id, phone=phone, 
                         topup_phone=topup_phone, topup_name=topup_name,
                         amount=amount, quantity=quantity,
                         type=type, lang=lang,
                         ref_name=ref_name, ref_phone=ref_phone,
                         mrule=mrule, promo=promo, new_cust_bonus=new_cust_bonus,
                         merchantname=merchantname, merchantid=merchantid)
        
        meta_data = {'remote_addr': kwargs.get('header__remote_addr'),
                     'timeout': kwargs.get('timeout')}
        meta_data.update(kwargs)
        result = self.call_service(self.HTTP_POST, url, params=None, **meta_data)
        
        return result
    
    def validate_raw_order(self, sku, notify=False, **kwargs):
        kwargs['Amount'] = 0
        return self.make_raw_order(sku, notify, **kwargs)
    
    def make_topup_order(self, country, carrier, cid=None, notify=False, **kwargs):
        '''
        Make an Top-Up order.
        - notify: Notify by SMS to customer
        - country: Country
        - carrier: Carrier Id
        - cid: A unique number to avoid repeated order
        - kwargs['card_id']: Id of credit card
        - kwargs['phone']: Customer phone
        - kwargs['topup_phone']: Phone to make Top-Up order
        - kwargs['topup_name']: 
        - kwargs['amount']: Order amount, default = 0
        - kwargs['phone_type']: Phone type of order, value = [cell, landline]
        - kwargs['lang']: Language of phone number, default = xx
        - kwargs['mrule']: Rule
        '''
        
        uuid_str = cid if cid else uuid.uuid1().__str__()
        
        card_id = ('&card_id=' + kwargs.get('card_id')) if kwargs.get('card_id') else ''
        phone = ('&phone=' + kwargs.get('phone')) if kwargs.get('phone') else ''
        topup_phone = ('&topup_phone=' + kwargs.get('topup_phone')) if kwargs.get('topup_phone') else ''
        topup_name = ('&topup_name=' + kwargs.get('topup_name')) if kwargs.get('topup_name') else ''
        amount = ('&amount=' + str(kwargs.get('amount'))) if kwargs.get('amount') else ''
        type = ('&phone_type=' + kwargs.get('phone_type')) if kwargs.get('phone_type') else ''
        lang = ('&lang=' + kwargs.get('lang')) if kwargs.get('lang') else ''
        mrule = ('&mrule=' + kwargs.get('mrule')) if kwargs.get('mrule') else ''
        
        url = 'PosService.svc/sellers/{0}/orders/{cid}/country/{country}/carrier/{carrierid}?notify={notify}'
        url += '{card_id}{phone}{topup_phone}{topup_name}{amount}{type}{lang}{mrule}'
        
        url = url.format(self.get_entity_user(),
                         cid=uuid_str,
                         country=country, carrierid=carrier, 
                         notify=self.__get_notify(notify),
                         card_id=card_id, phone=phone, 
                         topup_phone=topup_phone, topup_name=topup_name,
                         amount=amount,
                         type=type, lang=lang,
                         mrule=mrule)
        
        meta_data = {'remote_addr': kwargs.get('header__remote_addr'),
                     'timeout': kwargs.get('timeout')}
        result = self.call_service(self.HTTP_POST, url, params=None, **meta_data)
        
        return result
    
    def void_tx(self, txid, notify=False):
        
        url = 'PosService.svc/sellers/{0}/trans/{1}?notify={2}'
        url = url.format(self.get_entity_user(), txid, self.__get_notify(notify))
        
        result = self.call_service(self.HTTP_POST, url, params=None)
        
        return result
    
    def get_creditcards(self, pin):
        '''
        Get a list of CreditCards for an account.
        - pin: PIN of customer
        '''
        url = 'PosService.svc/cc/?pin={0}'
        url = url.format(pin)
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result
    
    def get_creditcard(self, cc_id):
        '''
        Get a list of CreditCards for an account.
        - pin: PIN of customer
        '''
        url = 'PosService.svc/cc/{0}'
        url = url.format(cc_id)
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result
    
    def add_creditcard(self, **kwargs):
        '''
        Add a cc
        '''
        url = 'PosService.svc/cc/'
        result = self.call_service(self.HTTP_POST, url, kwargs)
        
        return result
    
    def update_creditcard(self, id, **kwargs):
        '''
        update cc
        '''
        url = 'PosService.svc/cc/{0}'
        url = url.format(id)
        result = self.call_service(self.HTTP_PUT, url, kwargs)
        
        return result
        
    def delete_creditcard(self, id, notify=False):
        '''
        Delete cc
        '''
        url = 'PosService.svc/cc/{0}'
        url = url.format(id)
        self.call_service(self.HTTP_DELETE, url, params=None)
        
    def get_seller(self, seller, **kwargs):
        '''
        Get a list of CreditCards for an account.
        - seller: Seller name or Id
        '''
        url = 'PosService.svc/sellers/{0}'
        url = url.format(seller)
        company = ('?companyid=%s' % kwargs.get('company_id')) if kwargs.get('company_id') else ''
        url += company
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result
        
    def is_account_updated_since_tx(self, txid):
        '''
        Check if an check if there are any other modification to the customer account after tx_id 1 = Changes after tx_id 0 = No changes -1 = Cannot determine, 
        because it is a topup transaction, or tx_id did not do any update or valid transaction -100 = System error. Unexpected error happens
        '''
        url = 'PosService.svc/sellers/{0}/postacctupdate/?tx_id={1}'
        url = url.format(self.get_entity_user(), txid)
        
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result
    
    def get_products(self, sku='', prefix=''):
        url = 'PosService.svc/products/?sku={0}&prefix={1}'
        url = url.format(sku, prefix)
        
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result
    
    def get_product_sku(self, t='', phone=''):
        url = 'PosService.svc/sellers/{0}/skus?type={1}&phone={2}'
        url = url.format(self.get_entity_user(), t, phone)
        
        result = self.call_service(self.HTTP_GET, url, params=None)
        
        return result
    
    def mark_used(self, pin, amount, used_date, outpin, **kwargs):
        url = 'PosService.svc/sellers/{0}/pin/{1}?amount={2}&used_date={3}&outpin={4}'
        used_date_str = used_date.strftime('%Y%m%d%H%M%S') if used_date else ''
        url = url.format(self.get_entity_user(), pin, '%.2f' % amount, used_date_str, outpin)
        
        meta_data = {'remote_addr': kwargs.get('header__remote_addr')}
        result = self.call_service(self.HTTP_PUT, url, params=None, **meta_data)
        
        return result

    def __get_notify(self, notify):
        result = ''
        if str(notify).lower() in ['sms', 'true']:
            result = 'sms'
        
        return result
    
    def get_cdrs(self, pin, from_date, to_date, type='', **kwargs):
        url = 'PosService.svc/cdrs/?pin={0}&from_date={1}&to_date={2}&type={3}'
        url = url.format(pin, from_date, to_date, type)
        result = self.call_service(self.HTTP_GET, url, kwargs)
        
        return result
    
    def get_retailrates(self, sku, phone, country='', prefix='', filter='', **kwargs):
        url = 'PosService.svc/retailrates/?sku={0}&phone={1}&country={2}&filter={3}&prefix={4}'
        url = url.format(sku, phone, country, filter, prefix)
        result = self.call_service(self.HTTP_GET, url, kwargs)
        return result
    
    def get_order_status(self, cid):
        url = 'PosService.svc/sellers/{0}/orderstatus/{1}'
        url = url.format(self.get_entity_user(), cid)
        result = self.call_service(self.HTTP_GET, url)
        return result
    