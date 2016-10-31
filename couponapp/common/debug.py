

__all__ = [
        'trace',
        'log_conn_sql',
        ]


from functools import wraps
import logging
import pprint
import sys


def trace(f):
    name = f.__name__
    @wraps(f)
    def wrapper(*args, **kwds):
        buffer = []
        for a in args:
            buffer.append(pprint.pformat(a, indent=4))
        for (k, v) in kwds.items():
            buffer.append('%s=%s' % (k, pprint.pformat(a, indent=4)))
        logging.debug('TRACE IN  %s(%s)', name, ', '.join(buffer))
        try:
            result = f(*args, **kwds)
        except Exception, e:
            logging.exception('TRACE ERR %s', name)
            raise
        else:
            logging.debug('TRACE OUT %s => %s', name, pprint.pformat(result, indent=4))
            return result
    return wrapper

# Use snippet from 
# http://www.djangosnippets.org/snippets/290/
def log_conn_sql():
    from django.db import connection
    from django.conf import settings
    from lunex.common import log

    if len(connection.queries) > 0 and settings.DEBUG:
        width = 10000
        indentation = 2
        total_time = 0.0
        for query in connection.queries:
            nice_sql = query['sql'].replace('"', '').replace(',',', ')
            sql = "[%s] %s" % (query['time'], nice_sql)
            total_time = total_time + float(query['time'])
            while len(sql) > width-indentation:
                log.debug("%s%s" % (" "*indentation, sql[:width-indentation]))
                sql = sql[width-indentation:]
            log.debug("%s%s\n" % (" "*indentation, sql))
        replace_tuple = (" "*indentation, str(total_time))
        log.debug("%s[TOTAL TIME: %s seconds]" % replace_tuple)
