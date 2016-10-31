'''
Created on Sep 6, 2011

@author: KhoaTran
'''

import DjangoEnvironment
from lunex.common.v2.services.pos.models import Account, RegisteredPhone, SpeedDial
from lunex.common.v2.services.pos.api import PosService
from lunex.common.v2.services import utils

class EntityPosService(PosService):
    def get_entity_user(self):
        return self.entity_user.EntityName

def db_logger_func(entity_user, method, url, params, result):
    #EcsLog.log(entity_user, method, 
    #           '{0} {1}'.format(url, str(params)), str(result))
    pass
    
def get_pos_service(entity_user):
        return EntityPosService(entity_user, 
                                'http://test-api.lunextelecom.com/')

if __name__ == '__main__':
    #entt = ExEntity.objects.get(EntityName__iexact='LIT1A004')
    
    Account.load_pos_service('LIT1A004', 
                             url='http://test-api.lunextelecom.com/')
    
    print '== Get account by SKU and Phone number'
    
    account = Account.get('1000', '6786349090')
    print account.to_dict()
    print account.FirstName, account.LastName
    
    print '== Get account by PIN'
    
    #Account.load_pos_service(entt, get_srv_func=get_pos_service, reload=True)
    
    account2 = Account.get_by_pin(account.Pin)
    print account2.to_dict()
    print account2.FirstName, account.LastName

    print '== account2.get_register_phones'    
    reg_phone_lst = account2.get_registered_phones()
    for reg_phone in reg_phone_lst:
        print reg_phone.AccessPhone, reg_phone.Created, reg_phone.Phone
        print reg_phone.to_dict()
    
    print '== account2.get_register_phone'    
    reg_phone = account2.get_registered_phone('6786349111')
    print reg_phone.AccessPhone, reg_phone.Created, reg_phone.Phone
    print reg_phone.to_dict()
    
    print '== account2.update_registered_phone'
    new_reg_phone = RegisteredPhone(Phone='6786342222',
                                    Language='vi',
                                    Description='Add new reg phone')
    
    account2.update_registered_phone(new_reg_phone)
    
    print '== account2.delete_registered_phone'
    account2.delete_registered_phone(new_reg_phone.Phone)
    print 'Deleted registered phone'
    
    print '== account2.get_speed_dials'    
    spdl_lst = account2.get_speed_dials()
    for spdl in spdl_lst:
        print spdl.AccessPhone, spdl.Num, spdl.Phone
        print spdl.to_dict()
        
    print '== account2.get_speed_dial'    
    spdl = account2.get_speed_dial(1)
    print spdl.AccessPhone, spdl.Num, spdl.Phone
    print spdl.to_dict()
    
    print '== account2.update_speed_dial'
    new_spdl = SpeedDial(Phone='840838345752',
                         Description='Add new speed dial 3',
                         Num=3)
    
    spdl = account2.update_speed_dial(new_spdl)
    print spdl.AccessPhone, spdl.Num, spdl.Phone
    print spdl.to_dict()
    
    print '== account2.delete_speed_dial'
    account2.delete_speed_dial(3)
    print 'Deleted speed dial'
    
    srv = utils.ServiceLoader.get_pos_service('LIT1A004', 
                                              url='http://test-api.lunextelecom.com/')
    
    print '== srv.make_raw_order'
    kwargs = {'Phone': '6786349090',
              'Amount': 10}
    result = srv.make_raw_order('1000', **kwargs)
    print result
    
    