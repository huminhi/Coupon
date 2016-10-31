'''
Created on Dec 8, 2011

@author: KhoaTran
'''

import sys, commands, os, time
#from lunex.common import log
#logger = log.setup_logger('reload_app')

apps = [('TopUp', 'topup_gw'), 
        ('DID', 'didgw'), 
        ('SMS GW Incoming', 'smsingw'), 
        ('SMS GW Outgoing', 'smsgw'),
        ('Call GW', 'callgw'),
        ('Promo GW', 'promogw'),
        ('Incomm GW', 'incommgw'),
        ('Velocity GW', 'velocitygw'),
        ]

def main(args):
    user = 'lunex'
    pids = []
    if len(args) == 2:
        if args[1].lower() == 'list':
            print 'Apps:'
            print apps
    elif len(args) >= 3:
        if len(args) == 4:
            user = args[3]
        if args[1].lower() == 'view':
            pids = get_pids(args[2], user)
            print 'PIDs: %s' % ' '.join(pids)
        elif args[1].lower() == 'reload':
            pids = get_pids(args[2], user)
            print 'Old PIDs: %s' % ' '.join(pids)
            for pid in pids:
                kill_pid(pid)
            print 'Reloading...'
            time.sleep(1)
            pids = get_pids(args[2], user)
            print 'Reloaded. New PIDs: %s' % ' '.join(pids)
            
def get_pids(app_name, user='www-data'):
    result = []
    cmm_result = commands.getoutput('ps ax -f | grep %s' % app_name)
    #logger.debug(cmm_result)
    lines = cmm_result.split('\n')
    #print 'Lines: ', lines
    for line in lines:
        stripped_line = ' '.join(line.strip().split())
        cmds = stripped_line.split(' ')
        #print 'Commands ', cmds
        if cmds[0] == user and cmds[8] == app_name:
            result.append(cmds[1])
        
    return result

def reload(app_name, user='www-data'):
    pids = get_pids(app_name, user)
    #logger.debug('Old PIDs: %s' % str(pids))
    for pid in pids:
        kill_pid(pid)
    time.sleep(1)
    #logger.debug('Reloaded')
    pids = get_pids(app_name, user)
    #logger.debug('New PIDs: %s' % str(pids))
    return pids
        
def kill_pid(pid):
    try:
        #logger.debug('Killing %s' % pid)
        os.system('kill -9 %s' % pid)
    except Exception, ex:
        #logger.exception(ex)
        pass
    
if __name__ == "__main__":    
    try:
        main(sys.argv)
    except Exception as inst:
        print str(inst)