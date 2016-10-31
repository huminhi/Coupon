'''
Created on Sep 15, 2010

@author: khoatran
'''

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

def load_class(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured, 'Error importing authentication backend %s: "%s"' % (module, e)
    except ValueError, e:
        raise ImproperlyConfigured, 'Error importing authentication backends. Is AUTHENTICATION_BACKENDS a correctly defined list or tuple?'
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured, 'Module "%s" does not define a "%s" authentication backend' % (module, attr)
    return cls