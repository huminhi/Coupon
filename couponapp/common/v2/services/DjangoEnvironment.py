'''
Created on Sep 18, 2010

@author: haonguyen
'''
#!/usr/bin/python
import sys, os;
#Setting up environment
basedir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)));
#Automatically detect $sms_gw/src path
print basedir
sms_gw_path = os.path.normpath(os.path.join(basedir,''))
#uncomment to set sms_gw_path manually
#sms_gw_path = '/media/Data/Source/Lunex/SMS_GW/django1_1/src/'

os.environ['DJANGO_SETTINGS_MODULE'] = 'lunex.services.settings'
#sys.path.append(os.path.abspath('/usr/local/django'))
sys.path.append(os.path.abspath(sms_gw_path))

DEBUG_MODE = True;