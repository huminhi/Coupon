'''
Created on Sep 6, 2011

@author: KhoaTran
'''
import copy
from decimal import Decimal
from lunex.common.v2.services import utils, ServiceNotLoad, ApiError

class PosObject(utils.DictObject):
    __service = None
    __entity_user = None
    
    class DoesNotExist(Exception):
        pass
    
    class AlreadyExist(Exception):
        pass

    @staticmethod
    def get_pos_service(seller=''):
        '''
        Safe way to get POS service.
        '''
        if PosObject.__service is None:
            raise ServiceNotLoad
        if seller:
            return PosObject.clone_pos_service(seller)
        return PosObject.__service

    @staticmethod
    def clone_pos_service(seller=''):
        clone = copy.deepcopy(PosObject.__service)
        clone.entity_user = seller
        return clone
    
    @staticmethod
    def load_pos_service(entity_user, url='', logger_func=None, get_srv_func=None, reload=False, **kwargs):
        '''
        Load POS service before being able to using it.
         - entity_user: Entity that uses the service
         - url: URL of POS service
         - logger_func: Hook function used to log request and response of service
         - get_srv_func: User-defined function to get POS service. 
         It will skip "url" and "logger_func" parameters.
         - reload: Reload the service.   
        '''
        if PosObject.__service is None or reload:
            if get_srv_func is None:
                srv = utils.ServiceLoader.get_pos_service(entity_user, url, logger_func, **kwargs)
            else:
                srv = get_srv_func(entity_user)
                
            PosObject.__service = srv
            PosObject.__entity_user = entity_user
        
class PosLanguage(object):
    DEFAULT = 'xx'
    CAMPUDIAN = 'ca'
    CHINESE = 'ch'
    ENGLISH = 'en'
    KOREAN = 'de'
    SPANISH = 'sp'
    
class PosPhoneType(object):
    CELL = 'cell'
    LANDLINE = 'land'

class AccountUnlimitedStatus(object):
    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    
class RegisteredPhone(PosObject):
    '''
    POS registered phone
    '''
    def __init__(self, **kwargs):
        self.AccessPhone = ''
        self.Created = ''
        self.CreatedBy = ''
        self.Description = ''
        self.IsMain = False
        self.Language = ''
        self.Phone = ''
        self.PhoneType = ''
        self.Region = '' 
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.AccessPhone = str(self.AccessPhone)
        self.Created = utils.get_json_datetime(self.Created, self.Created)
        self.CreatedBy = str(self.CreatedBy)
        self.Description = str(self.Description)
        self.IsMain = utils.get_boolean(self.IsMain)
        self.Language = str(self.Language)
        self.Phone = str(self.Phone)
        self.PhoneType = str(self.PhoneType)
        self.Region = str(self.Region)

class SpeedDial(PosObject):
    '''
    POS speed dial
    '''
    def __init__(self, **kwargs):
        self.AccessPhone = ''
        self.AccessPhoneInt = ''
        self.Description = ''
        self.Num = 0
        self.Phone = ''
        self.Region = ''
        self.RegionInt = ''
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.AccessPhone = str(self.AccessPhone)
        self.AccessPhoneInt = str(self.AccessPhoneInt)
        self.Description = str(self.Description)
        self.Num = utils.get_int(self.Num)
        self.Phone = str(self.Phone)
        self.Region = str(self.Region)
        self.RegionInt = str(self.RegionInt)

class CDR(PosObject):
    '''
    POS speed dial
    '''
    def __init__(self, **kwargs):
        self.AccessPhone = ''
        self.Ani = ''
        self.Balance = 0
        self.CalledTime = ''
        self.Carrier = ''
        self.Charge = 0
        self.Destination = ''
        self.Duration = 0
        self.RoundDuration = 0
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.AccessPhone = str(self.AccessPhone)
        self.Ani = str(self.Ani)
        self.Balance = utils.get_decimal(self.Balance)
        self.CalledTime = utils.get_json_datetime(self.CalledTime, self.CalledTime)
        self.Carrier = str(self.Carrier)
        self.Charge = utils.get_decimal(self.Charge)
        self.Destination = str(self.Destination)
        self.Duration = utils.get_decimal(self.Duration)
        self.RoundDuration = utils.get_decimal(self.RoundDuration)
        
class Merchant(PosObject):
    def __init__(self, **kwargs):
        self.Amount = 0
        self.AuthCode = ''
        self.AuthResp = ''
        self.Message = ''
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.Amount = utils.get_int(self.Amount)

class OrderDetail(PosObject):
    
    def __init__(self, **kwargs):
        self.AcctBalance = 0
        self.AcctNum = ''
        self.AcctType = ''
        self.Amount = 0
        self.Balance = 0
        self.Bonus = 0
        self.PaymentType = ''
        self.Phone = ''
        self.Pins = None
        self.Quantity = 0
        self.Sku = ''
        self.Status = ''
        self.Time = ''
        self.TopupCode = ''
        self.TopupCountry = ''
        self.TopupCountryCode = ''
        self.TopupName = ''
        self.TopupOperatorCode = ''
        self.TopupOperator = ''
        self.TopupPin = ''
        self.TopupPhone = ''
        self.TxId = 0
        
        self.set_value(**kwargs)
    
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.AcctBalance = utils.get_decimal(self.AcctBalance)
        self.Amount = utils.get_decimal(self.Amount)
        self.Bonus = utils.get_decimal(self.Bonus)
        self.Balance = utils.get_decimal(self.Balance)
        self.Quantity = utils.get_int(self.Quantity)
        self.Time = utils.get_json_datetime(self.Time, self.Time)
        self.TxId = utils.get_int(self.TxId)

class Order(PosObject):
    '''
    POS Order
    '''
    
    def __init__(self, **kwargs):
        self.Merchant = None
        self.Message = None
        self.Code = 0
        self.Order = None
        self.Merchant = None
        self.Time = None
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.Message = utils.get_str(self.Message)
        self.Code = utils.get_int(self.Code)
        self.Time = utils.get_json_datetime(self.Time, self.Time)
        if not isinstance(self.Order, OrderDetail):
            self.Order = OrderDetail(**(kwargs['Order']))
            
        if not isinstance(self.Merchant, Merchant) and kwargs.get('Merchant'):
            self.Merchant = Merchant(**(kwargs['Merchant']))

class OrderStatus(PosObject):
    def __init__(self, **kwargs):
        self.Cid = None
        self.Message = None
        self.Status = None
        self.Time = None
        self.TxId = None
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        
        self.Time = utils.get_json_datetime(self.Time, self.Time)
        utils.DictObject.set_value(self, **kwargs)

class Address(PosObject):
    def __init__(self, **kwargs):
        self.City = None
        self.Country = None
        self.State = None
        self.Street = None
        self.Suite = None
        self.Zipcode = None
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)

class Card(PosObject):
    def __init__(self, **kwargs):
        self.Code = None
        self.Expire = None
        self.FullName = None
        self.Num = None
        self.Type = None
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)

class CreditCard(PosObject):
    '''
    POS CreditCard
    '''
    
    def __init__(self, **kwargs):
        self.Address = None
        self.Card = None
        self.FirstName = ''
        self.Id = 0
        self.IsDefault = False
        self.LastName = ''
        self.Name = ''
        self.Phone = ''
        self.Pin = 0
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.FirstName = str(self.FirstName)
        self.IsDefault = utils.get_boolean(self.IsDefault)
        self.LastName = str(self.LastName)
        self.Name = str(self.Name)
        self.Phone = str(self.Phone)
        self.Pin = utils.get_int(self.Pin)
        
        if not isinstance(self.Address, Address) and kwargs.get('Address'):
            self.Address = Address(**(kwargs['Address']))
        
        if not isinstance(self.Card, Card) and kwargs.get('Card'):
            self.Card = Card(**(kwargs['Card']))

    @staticmethod
    def get(cc_id):
        '''
        Get CC from API.
        '''
        cc = CreditCard()
        try:
            dict_cc = PosObject.get_pos_service().get_creditcard(cc_id)
        except ApiError, ex:
            if ex.code == -21:
                raise CreditCard.DoesNotExist
            
        cc.set_value(**dict_cc)
        
        return cc
      
class Account(PosObject):
    '''
    POS customer account
    '''
    def __init__(self, seller='', **kwargs):
        self.Balance = Decimal('0')
        self.City = ''
        self.Created = ''
        self.CreatedBy = ''
        self.Currency = ''
        self.Email = ''
        self.FirstName = ''
        self.LastName = ''
        self.MinBalance = Decimal('0')
        self.Notes = ''
        self.Phone = ''
        self.Pin = 0
        self.ReferralName = ''
        self.ReferralPhone = ''
        self.Promo = ''
        self.RefillAmt = Decimal('0')
        self.Sku = ''
        self.State = ''
        self.StatementOption = 'NONE'
        self.Street = ''
        self.Zipcode = ''
        #Unlimited
        self.ExpiredDate = None
        self.Minutes = None
        self.Status = None
        #Redeem Pin
        self.FirstUseDate = None
        self.RedeemDate = None
        self.Reseller = ''

        self.__service = PosObject.get_pos_service(seller)
        self.set_value(**kwargs)
    
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.Balance = utils.get_decimal(self.Balance)
        self.City = str(self.City)
        self.Created = utils.get_json_datetime(self.Created, self.Created)
        self.CreatedBy = str(self.CreatedBy)
        self.Currency = str(self.Currency)
        try: 
            self.Email = self.Email 
        except: 
            self.Email = ''
        try: 
            self.FirstName = self.FirstName
        except:
            self.FirstName = ''
        try:
            self.LastName = self.LastName
        except:
            self.LastName = ''
        self.MinBalance = utils.get_decimal(self.MinBalance)
        try:
            self.Notes = self.Notes
        except:
            self.Notes = ''
        self.Phone = str(self.Phone)
        self.Pin = utils.get_int(self.Pin)
        try:
            self.ReferralName = self.ReferralName
        except:
            self.ReferralName = ''
        self.ReferralPhone = str(self.ReferralPhone)
        self.Promo = str(self.Promo)
        self.RefillAmt = utils.get_decimal(self.RefillAmt)
        self.Sku = str(self.Sku)
        self.State = str(self.State)
        self.StatementOption = str(self.StatementOption)
        try:
            self.Street = self.Street
        except:
            self.Street = ''
        self.Zipcode = str(self.Zipcode)
        #Unlimited
        self.ExpiredDate = utils.get_json_datetime(self.ExpiredDate, self.ExpiredDate)
        self.Minutes = int(self.Minutes) if self.Minutes else None
        self.Status = str(self.Status) if self.Status else None
        #Redeem Pin
        self.FirstUseDate = utils.get_json_datetime(self.FirstUseDate, self.FirstUseDate)
        self.RedeemDate = utils.get_json_datetime(self.RedeemDate, self.RedeemDate)
        self.Reseller = str(self.Reseller)

    @staticmethod
    def get(sku, phone, seller=''):
        '''
        Get account from API.
        - sku: SKU of phone that customer account registered
        - phone: Main registered phone of customer account
        '''
        account = Account(seller)
        try:
            dict_account = PosObject.get_pos_service(seller).get_account(sku, phone)
        except ApiError, ex:
            if ex.code == -21:
                raise Account.DoesNotExist

        account.set_value(**dict_account)

        return account

    @staticmethod
    def get_by_pin(pin, seller=''):
        '''
        Get account from API.
        - pin: PIN of customer
        '''
        account = Account(seller)
        dict_account = PosObject.get_pos_service(seller).get_account_by_pin(pin)
        account.set_value(**dict_account)

        return account

    @staticmethod
    def get_by_pins(pins=[], seller=''):
        '''
        Get account from API.
        - pin: PIN of customer
        '''
        accounts = []
        pos_accounts = PosObject.get_pos_service(seller).get_account_by_pins(pins)
        for pos_account in pos_accounts:
            account = Account(seller)
            account.set_value(**pos_account)
            accounts.append(account)

        return accounts
    
    def refresh(self):
        dict_account = Account.get_pos_service().get_account_by_pin(self.Pin)
        self.set_value(**dict_account)
    
    def order(self, sku, amount=0, cid=None, notify=False, **kwargs):
        order = Seller.order(self.Phone, sku, amount, cid, notify, **kwargs)
        self.refresh()
        
        return order
    
    def order_pin(self, sku, quantity=0, cid=None, notify=False, **kwargs):
        order = Seller.order_pin(self.Phone, sku, quantity, cid, notify, **kwargs)
        self.refresh()
        
        return order
    
    @staticmethod
    def order_promocode(phone, sku, promo_code, cid=None, notify=False, **kwargs):
        order = Seller.order_promocode(phone, sku, promo_code, cid, notify, **kwargs)        
        return order
    
    def void_order(self, txid, notify=False):
        order = Seller.void_order(txid, notify)
        self.refresh()
        
        return order
    
    def save(self, notify=False, **kwargs):
        '''
        Save account to API
        - kwargs['lang']: Language of main registered phone number
        - kwargs['phone_type']: Phone type of main registered phone number
        - kwargs['promo']: Promotion code
        - kwargs['new_cust_bonus']: New customer bonus
        - kwargs['ref_name']: Referral name
        - kwargs['ref_phone']: Referral phone
        '''
        account_dict = {'Balance': 0,
                        'City': self.City,
                        'Currency': self.Currency,
                        'Email': self.Email,
                        'FirstName': self.FirstName,
                        'LastName': self.LastName,
                        'MinBalance': float(str(self.MinBalance)),
                        'Notes': self.Notes,
                        'Phone': self.Phone,
                        'ReferralName': self.ReferralName,
                        'ReferralPhone': self.ReferralPhone,
                        'RefillAmt': float(str(self.RefillAmt)),
                        'Sku': self.Sku,
                        'State': self.State,
                        'StatementOption': self.StatementOption,
                        'Street': self.Street,
                        'Zipcode': self.Zipcode
                        }
        new_account = self.__service.update_account(self.Sku, self.Phone, account_dict, notify, **kwargs)
        self.set_value(**new_account)
        
    def update_account_original_retailer(self, retailer='', **kwargs):
        '''
        Update orignal retailer
        '''
        if retailer:
            new_account = self.__service.update_account_original_retailer(self.Sku, self.Phone, retailer=retailer)
            self.set_value(**new_account)
        return []
        
    def save_unlimited_status(self, status, minutes=None, expired_date=None):
        dict_account = self.__service.update_unlimited_status(self.Pin, status, minutes, expired_date)
        #dict_account = self.__service.get_account(self.Sku, self.Phone)
        self.set_value(**dict_account)
        
    def get_registered_phones(self):
        '''
        Get a list of registered phone for an account.
        '''
        lst = self.__service.get_registered_phones(self.Pin)
        
        result = []
        for item in lst:
            reg_phone = RegisteredPhone(**item)
            result.append(reg_phone)
            
        return result
    
    def get_registered_phone(self, phone):
        '''
        Get a registered phone for an account.
        '''
        item = self.__service.get_registered_phone(self.Pin, phone)
        if item is None:
            raise RegisteredPhone.DoesNotExist
        reg_phone = RegisteredPhone(**item)
            
        return reg_phone
    
    def update_registered_phone(self, reg_phone_obj, notify=False):
        '''
        Add/update a registered phone for an account.
        '''
        data = {'Description': reg_phone_obj.Description, 
                'Language': reg_phone_obj.Language, 
                'IsMain': reg_phone_obj.IsMain,
                'Phone': reg_phone_obj.Phone,
                'PhoneType': reg_phone_obj.PhoneType}
        
        item = self.__service.update_registered_phone(self.Pin, notify,
                                                      **data)
        
        reg_phone = RegisteredPhone(**item)
            
        return reg_phone
    
    def delete_registered_phone(self, phone, notify=False):
        '''
        Delete a registered phone. If a main number is deleted, 
        the next one in the list will become main.
        '''
        self.__service.delete_registered_phone(self.Pin, 
                                               phone, notify)
        
    def get_speed_dials(self):
        '''
        Get a list of speed dials for an account.
        '''
        lst = self.__service.get_speed_dials(self.Pin)
        
        result = []
        for item in lst:
            spdl = SpeedDial(**item)
            result.append(spdl)
            
        return result
    
    def get_speed_dial(self, num):
        '''
        Get a speed dial for an account.
        '''
        item = self.__service.get_speed_dial(self.Pin, num)
        if item is None:
            raise RegisteredPhone.DoesNotExist
        spdl = SpeedDial(**item)
        
        return spdl
    
    def update_speed_dial(self, spdl_obj, auto=False, notify=False):
        '''
        Add/update a speed dial for an account.
        - auto: Auto pick Speed Dial Number to add/update speed dial. 
        If updating information is not different from current information,
        a DestinationPhoneExist exception will be raised.
        '''
        data = {'Description': spdl_obj.Description,
                'Phone': spdl_obj.Phone,
                'Num': spdl_obj.Num,
                }
        
        if auto:
            data['Num'] = self.__auto_pick_speed_dial_number(spdl_obj)
            if data['Num'] == 0:
                raise SpeedDial.AlreadyExist
            
        item = self.__service.update_speed_dial(self.Pin, notify, **data)
        
        spdl = SpeedDial(**item)
            
        return spdl
    
    def __auto_pick_speed_dial_number(self, spdl_obj):
        num = 1
        is_new = True
        is_update = True
        spdl_objs = self.get_speed_dials()
        for item in spdl_objs:
            if spdl_obj.Phone == str(item.Phone):
                is_new = False
                if spdl_obj.Description == item.Description:
                    is_update = False
                break
            num += 1
            
        if is_new:
            num = 1
            for item in spdl_objs:
                if num != item.Num:
                    break
                num += 1
                
        if is_new or is_update:
            pass
        else:
            num = 0
        
        return num
    
    def delete_speed_dial(self, num, notify=False):
        '''
        Delete a speed dial.
        '''
        self.__service.delete_speed_dial(self.Pin, num, notify)    

    def get_creditcards(self):
        '''
        Get a list of speed dials for an account.
        '''
        lst = self.__service.get_creditcards(self.Pin)
        
        result = []
        for item in lst:
            cc = CreditCard(**item)
            result.append(cc)
            
        return result
    
    def get_creditcard(self, cc_id):
        '''
        Get a list of speed dials for an account.
        '''
        card = self.__service.get_creditcard(cc_id)
        cc = CreditCard(**card)
        
        return cc

    def add_creditcard(self, cc_obj, notify=False):
        '''
        Add cc for an account.
        '''
        data = cc_obj.to_dict()
        data['Card'] = data['Card'].to_dict()
        data['Address'] = data['Address'].to_dict()
        item = self.__service.add_creditcard(**data)
        cc = CreditCard(**item)
            
        return cc
    
    def update_creditcard(self, id, cc_obj, notify=False):
        '''
        Update cc for an account.
        '''
        data = cc_obj.to_dict()
        data['Card'] = data['Card'].to_dict()
        data['Address'] = data['Address'].to_dict()
        item = self.__service.update_creditcard(id, **data)
        cc = CreditCard(**item)
            
        return cc
    
    def delete_creditcard(self, id, notify=False):
        '''
        Delete a registered phone. If a main number is deleted, 
        the next one in the list will become main.
        '''
        self.__service.delete_creditcard(id)
        
    def get_cdrs(self, from_date, to_date, type='', **kwargs):
        lst = self.__service.get_cdrs(self.Pin, from_date, to_date, type)
        if not lst:
            lst = []
        result = []
        for item in lst:
            cc = CDR(**item)
            result.append(cc)
            
        return result
        
class Seller(PosObject):
    def __init__(self, **kwargs):
        self.__service = PosObject.get_pos_service()
        self.set_value(**kwargs)
    
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        if kwargs.has_key('Accounts'):
            self.__set_account('Prepaid', kwargs['Accounts'])
            self.__set_account('Postpaid', kwargs['Accounts'])
            self.__set_account('Prepaid_Bank', kwargs['Accounts'])
            self.__set_account('Postpaid_Bank', kwargs['Accounts'])
        
    def __set_account(self, account_name, accounts):
        for account in accounts:
            if account['AcctType'] == account_name.upper():
                setattr(self, account_name.replace('_', ''), Decimal(str(account['Balance'])))
        
    @staticmethod
    def get(seller_name):
        '''
        Get Seller from API.
        '''
        seller = Seller()
        try:
            dict_seller = PosObject.get_pos_service().get_seller(seller_name)
        except ApiError, ex:
            if ex.code == -12:
                raise Seller.DoesNotExist
            
        seller.set_value(**dict_seller['Entity'])
        
        return seller
    
    @staticmethod
    def order(phone, sku, amount=0, cid=None, notify=False, **kwargs):
        kwargs['phone'] = phone
        order = Seller.__inner_order(Account.get_pos_service().make_raw_order, sku, amount, cid, notify, **kwargs)
        return order
    
    @staticmethod
    def get_order_status(cid):
        dict_order_status = PosObject.get_pos_service().get_order_status(cid) 
        order_status = OrderStatus(**dict_order_status)
        return order_status
    
    @staticmethod
    def order_pin(phone, sku, quantity=0, cid=None, notify=False, **kwargs):
        kwargs['phone'] = phone
        kwargs['quantity'] = quantity
        order = Seller.__inner_order(Account.get_pos_service().make_raw_order, sku, None, cid, notify, **kwargs)
        return order
    
    @staticmethod
    def order_promocode(phone, sku, promo_code, cid=None, notify=False, **kwargs):
        kwargs['phone'] = phone
        kwargs['promo'] = promo_code
        kwargs['new_cust_bonus'] = 0
        order = Seller.__inner_order(Account.get_pos_service().make_raw_order, sku, None, cid, notify, **kwargs)
        return order
    
    @staticmethod
    def topup_order(phone, country_code, carrier_code, topup_phone, amount, cid=None, notify=False, **kwargs):
        kwargs['phone'] = phone
        kwargs['topup_phone'] = topup_phone
        kwargs['amount'] = amount
        dict_order = Account.get_pos_service().make_topup_order(country_code, carrier_code, **kwargs)
        order = Order(**dict_order)
        return order
    
    @staticmethod
    def void_order(txid, notify=False):
        dict_order = PosObject.get_pos_service().void_tx(txid, notify) 
        order = Order(**dict_order)
        return order 
        
    @staticmethod
    def is_account_updated_since_tx(txid):
        dict_order = PosObject.get_pos_service().is_account_updated_since_tx(txid)
        code = int(dict_order.get('Code', 0)) 
        return True if code == 1 else False
        
    @staticmethod
    def mark_used(pin, amount, used_date, outpin, **kwargs):
        result = PosObject.get_pos_service().mark_used(pin, amount, used_date, outpin, **kwargs)
        return result 
        
    @staticmethod
    def __inner_order(order_func, sku, amount=0, cid=None, notify=False, **kwargs):
        kwargs['amount'] = amount
        kwargs['quantity'] = 1
        dict_order = order_func(sku, cid, notify, **kwargs)
        order = Order(**dict_order)
        return order
    
class Product(PosObject):
    VENUE_LUNEX = 'lunex'
    VENUE_INCOMM = 'incomm'
    
    def __init__(self, **kwargs):
        self.CarrierCode = None
        self.CountryCode = None
        self.Currency = None
        self.DestAmt = 0
        self.MaxLen = 0
        self.MinLen = 0
        self.Name = None
        self.Sku = None
        self.SrcAmt = None
        self.Type = None
        self.DestSku = None
        self.Venue  = None
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.CarrierCode = int(self.CarrierCode) if self.CarrierCode else None
        self.MaxLen = int(self.MaxLen) if self.MaxLen else None
        self.MinLen = int(self.MaxLen) if self.MinLen else None
        self.Sku = str(self.Sku) if self.Sku else None
        self.DestSku = str(self.DestSku) if self.DestSku else None
        self.SrcAmt = Decimal(str(self.SrcAmt)) if self.SrcAmt else None
        
    @staticmethod
    def get(sku, prefix=''):
        '''
        Get Product by Sku from API.
        '''
        prod = Product()
        
        prods = PosObject.get_pos_service().get_products(sku, prefix)
        if len(prods) == 0:
            raise Product.DoesNotExist
        else:
            prod.set_value(**prods[0])
        
        return prod
    
    @staticmethod
    def list(sku, prefix):
        '''
        Get List of Product by Sku and filter from API.
        '''
        
        prods = PosObject.get_pos_service().get_products(sku, prefix)
        result = []
        for prod_dict in prods:
            prod = Product()
            prod.set_value(**prod_dict)
            result.append(prod)
            
        return result

class RetailRate(PosObject):
    '''
    POS RetailRate
    '''
    
    def __init__(self, **kwargs):
        self.CountryCode = ''
        self.CountryName = ''
        self.DidRate = Decimal('0')
        self.Id = ''
        self.LocationCode = ''
        self.LocationName = ''
        self.RateId = 0
        self.Sku = ''
        self.TollfreeRate = Decimal('0')
        self.Updated = ''
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.CountryCode = str(self.CountryCode)
        self.CountryName = str(self.CountryName)
        self.DidRate = utils.get_decimal(self.DidRate)
        self.Id = str(self.Id)
        self.LocationCode = str(self.LocationCode)
        self.LocationName = str(self.LocationName)
        self.RateId = utils.get_int(self.RateId)
        self.Sku = str(self.Sku)
        self.TollfreeRate = utils.get_decimal(self.TollfreeRate)
        self.Updated = utils.get_json_datetime(self.Updated, self.Updated)

    @staticmethod
    def get(sku, phone, country='', prefix='', filter='', **kwargs):
        '''
        Get RetailRates from API.
        '''
        try:
            dict_rate = PosObject.get_pos_service().get_retailrates(sku, phone, country, prefix, filter, **kwargs)
            result = []
            for item in dict_rate:
                rate = RetailRate(**item)
                result.append(rate)
        except ApiError, ex:
            if ex.code == -21:
                raise RetailRate.DoesNotExist
            
        return result
      
    @staticmethod
    def get_lowest(sku, phone, country='', prefix='', filter='', **kwargs):
        '''
        Get RetailRates from API.
        '''
        try:
            dict_rate = PosObject.get_pos_service().get_retailrates(sku, phone, country, prefix, filter, **kwargs)
            if len(dict_rate) > 0:
                best_rate = dict_rate[0]
            else:
                return {}
            
            for item in dict_rate:
                if item['DidRate'] < best_rate['DidRate']:
                    best_rate = item
        except ApiError, ex:
            if ex.code == -21:
                raise RetailRate.DoesNotExist
            
        return RetailRate(**best_rate)

class Amount(PosObject):
    def __init__(self, **kwargs):
        self.Amt = None
        self.Denom = None
        self.DestAmt = None
        self.DestCurr = None
        self.Fee = None
        self.Instruction = None
        self.MaxAmt = None
        self.MinAmt = None
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.Amt = utils.get_decimal(self.Amt)
        self.DestAmt = utils.get_decimal(self.DestAmt)
        self.Fee = utils.get_decimal(self.Fee)
        self.MaxAmt = utils.get_decimal(self.MaxAmt)
        self.MinAmt = utils.get_decimal(self.MinAmt)
        
class Product2(PosObject):
    def __init__(self, **kwargs):
        self.City = None
        self.CityCode = None
        self.Country = None
        self.CountryCode = None
        self.MaxLen = None
        self.MinLen = None
        self.Name = None
        self.Repl = None
        self.Sku = None
        self.Type = None
        self.SubProduct = None
        
        self.set_value(**kwargs)
        
    def set_value(self, **kwargs):
        '''
        Should use this method to set value of properties.
        '''
        utils.DictObject.set_value(self, **kwargs)
        
        self.MaxLen = utils.get_int(self.MaxLen)
        self.MinLen = utils.get_int(self.MinLen)
        self.SubProduct = utils.get_boolean(self.SubProduct)
        
        self.Amounts = []
        if kwargs.get('Amounts'):
            amounts = kwargs.get('Amounts')
            for amount in amounts:
                amount_obj = Amount(**amount)
                self.Amounts.append(amount_obj)
                
    @staticmethod
    def get(t='', phone=''):
        '''
        Get Product.
        '''
        prod_objs = []
        
        prods = PosObject.get_pos_service().get_product_sku(t, phone)
        if not prods:
            raise Product2.DoesNotExist
        else:
            for prod in prods:
                prod_obj = Product2()
                prod_obj.set_value(**prod)
                prod_objs.append(prod_obj)
        
        return prod_objs
        