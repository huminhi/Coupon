

"""\
This provides access to a database.

This loads the settings from a Python module. The module is identified by the
environment variable "LUNEX_SETTINGS_MODULE."

The settings module needs to contain these variables:

    - DATABASE_ENGINE;
    - DATABASE_HOST;
    - DATABASE_NAME;
    - DATABASE_USER; and
    - DATABASE_PASSWORD.

"""

__all__ = [
        'IsolationLevel',
        'ConnectionSettings',
        'noconstraints',
        'transaction_isolation',
        'make_cxn_string',
        'make_db_url',
        'new_cxn',
        'get_cxn',
        'set_cxn',
        'cursor',
        'transaction',
        'commit_on_success',
        'execute',
        'executemany',
        'scalar_query',
        'query',
        'pp',
        ]


from collections import defaultdict, namedtuple
from contextlib import closing, contextmanager
from functools import wraps
import logging
import os
import pprint
import sys
import threading
import urllib
from lunex.common import runtime
from django.db import connection
import pyodbc

from lunex.common.enum import Enum
from lunex.common import coerce_types


##########################
## Loading the settings ##
##########################


LUNEX_SETTINGS_MODULE_KEY = 'LUNEX_SETTINGS_MODULE'
_settings = None
def get_settings():
    global _settings
    if _settings is None:
        if LUNEX_SETTINGS_MODULE_KEY not in os.environ:
            raise Exception, 'No value for LUNEX_SETTINGS_MODULE'
        lunex_settings_module = os.environ[LUNEX_SETTINGS_MODULE_KEY]
        logging.info('Loading Lunex settings from "%s"', lunex_settings_module)
        try:
            _settings = __import__(lunex_settings_module)
        except ImportError:
            raise Exception, 'Invalid value for LUNEX_SETTINGS_MODULE: "%s"' % (lunex_settings_module,)
    return _settings


##########################
## Thread-Local Storage ##
##########################


local = threading.local()


#################
## Constraints ##
#################


@contextmanager
def noconstraints(cxn, tables):
    """\
    This lifts the foreign key constraints on a set of tables during a context.

    """

    cursor_factory = (cxn._cursor if hasattr(cxn, '_cursor') else cxn.cursor)
    c = cursor_factory()
    fkeys = defaultdict(list)
    for tbl in tables:
        for fk in c.foreignKeys(tbl):
            fkeys[fk[6]].append(fk[-3])
    for (tbl, fks) in fkeys.items():
        sql = 'ALTER TABLE %s NOCHECK CONSTRAINT %s' % (tbl, ','.join(fks))
        logging.info(sql)
        c.execute(sql)
    try:
        yield
    finally:
        for (tbl, fks) in fkeys.items():
            sql = 'ALTER TABLE %s CHECK CONSTRAINT %s' % (tbl, ','.join(fks))
            logging.info(sql)
            c.execute(sql)
        c.close()


class IsolationLevel(Enum):
    (READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SNAPSHOT,
            SERIALIZABLE) = range(5)

    @classmethod
    def get_level(cls, level):
        if isinstance(level, (int, long)):
            return level
        level = level.replace('_', ' ').title()
        return cls._label_index.get(level)


@contextmanager
def transaction_isolation(level, cxn=None):
    cxn = cxn or get_cxn()
    ilevel = IsolationLevel.get_level(level)
    level_label = IsolationLevel.get_label(ilevel)
    c = cxn.cursor()
    c.execute('DBCC USEROPTIONS;')
    current = [ o[1] for o in c if o[0].lower() == 'isolation level' ]
    c.execute('SET TRANSACTION ISOLATION LEVEL %s;' % (level_label,))
    try:
        yield
    finally:
        if current:
            c.execute('SET TRANSACTION ISOLATION LEVEL %s;' % (current[0],))
        c.close()


#############################
## The Interface Functions ##
#############################


ConnectionSettings = namedtuple(
    'ConnectionSettings',
    'DATABASE_ENGINE, DATABASE_DSN, DATABASE_HOST, DATABASE_NAME, DATABASE_USER, '
    'DATABASE_PASSWORD, DATABASE_TRUSTED'
    )

CXN_FIELDS = [
        ('DRIVER', 'DATABASE_ENGINE'),
        ('DSN', 'DATABASE_DSN'),
        ('SERVER', 'DATABASE_HOST'),
        ('DATABASE', 'DATABASE_NAME'),
        ('UID', 'DATABASE_USER'),
        ('PWD', 'DATABASE_PASSWORD'),
        ('Trusted_Connection', 'DATABASE_TRUSTED'),
        ]

ENGINE_SCHEMA = {
        'postgresql_psycopg2': 'postgres',
        'postgresql': 'postgres',
        'mysql': 'mysql',
        'sqlite3': 'sqlite',
        'oracle': 'oracle',
        'sql_server.pyodbc': 'mssql',
        }


def make_cxn_string(sets=None):
    if sets is None:
        sets = get_settings()
    cxn_fields = [
            '%s=%s;' % (f, getattr(sets, k))
            for (f, k) in CXN_FIELDS
            if getattr(sets, k, None)
            ]
    cxn_string = ' '.join(cxn_fields)
    return cxn_string


def make_db_url(sets=None):
    if sets is None:
        sets = get_settings()
    uri = '%s:///?odbc_connect=%s' % (
            ENGINE_SCHEMA.get(sets.DATABASE_ENGINE, 'mssql'),
            urllib.quote_plus(make_cxn_string(sets)),
            )
    return uri


def new_cxn(autocommit):
    cxn_string = make_cxn_string()
    logging.info('connecting to db %s', cxn_string)
    try:
        return pyodbc.connect(cxn_string, autocommit=autocommit)
    except:
        logging.error('ERROR with connection string = %r', cxn_string)
        raise


def get_cxn(force_new=False, autocommit=False):
    """\
    This gets the current connection, creating it if necessary.

    'force_new' forces the current database (if opened) to be closed and a new
    connection to be opened and returned;

    'autocommit' sets the autocommit variable on the connection.

    """

    if force_new:
        cxn = new_cxn(autocommit)
        set_cxn(cxn)
    else:
        try:
            cxn = local.cxn
        except AttributeError:
            cxn = new_cxn(autocommit)
            set_cxn(cxn)
    if callable(cxn):
        cxn = cxn()
    return cxn


def set_cxn(cxn):
    """\
    This sets the current connection.

    If there is already a connection open on this thread, it is closed first.

    """

    if getattr(local, 'cxn', None) != cxn:
        try:
            local.cxn.close()
        except:
            pass
    local.cxn = cxn


def cursor(cxn=None):
    """\
    This creates a new cursor, wrapped in contextlib.closing.

    This is meant to be used in a "with" context:

    >>> with cursor() as c:
    ...     c.execute('SELECT 1;')

    """

    cxn = cxn or get_cxn()
    return closing(cxn.cursor())


@contextmanager
def transaction(cxn=None):
    """\
    This executes code in a transaction context, returning a cursor.

    If the code throws an exception, the transaction is rolled back. If it
    completes successfully, the transaction is committed.

    >>> with transaction() as c:
    ...    c.execute('...')

    """

    cxn = cxn or get_cxn()
    c = cxn.cursor()
    try:
        yield c
    except:
        cxn.rollback()
        raise
    else:
        cxn.commit()
    finally:
        c.close()


def commit_on_success(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        with transaction():
            return f(*args, **kwds)
    return wrapper


def __try_call(func, sql, params):
    try:
        return func(sql, params)
    except:
        logging.error('SQL    = %s', sql)
        logging.error('params = %s', pprint.pformat(params))
        raise


def execute(sql, params=(), cxn=None):
    """\
    This executes a non-query SQL statement with parameters.

    >>> execute('CREATE TABLE names (first VARCHAR(32), last VARCHAR(32));')

    """

    with cursor() as c:
        return __try_call(c.execute, sql, params)


def executemany(sql, params=(), cxn=None):
    """\
    This executes a non-query SQL statement with multiple parameters.

    >>> executemany('INSERT INTO names (first, last) VALUES (?, ?);', [
    ... ('Jerry', 'Jung'), ('Tejas', 'Iyer'), ('Eric', 'Rochester')])

    """

    with cursor() as c:
        return __try_call(c.executemany, sql, params)


def scalar_query(sql, params=(), cxn=None, default=None):
    """\
    This executes a query and returns the first item of the first row.

    >>> scalar_query('SELECT COUNT(*) FROM TBLlogin;')

    """

    with cursor() as c:
        __try_call(c.execute, sql, params)
        row = c.fetchone()
        return (row[0] if row is not None else default)


def query(sql, params=(), cxn=None):
    """\
    This executes a query and returns an iterator over the result rows.

    >>> for c in query('SELECT * FROM TBLlogin;'):
    ...     print c

    NB: If you will be executing other SQL statements while this query is
    iterating, you may need to pull all the rows from the database using
    'list(query(...))'.

    """

    with cursor() as c:
        __try_call(c.execute, sql, params)
        for row in c:
            yield row


## From http://code.activestate.com/recipes/81189/
def pp(cursor, data=None, rowlens=False):
    d = cursor.description
    if not d:
        return "#### NO RESULTS ###"
    names = []
    lengths = []
    rules = []
    if data is None:
        data = cursor.fetchall()
    for dd in d:    # iterate over description
        l = dd[3]
        if not l:
            l = 12             # or default arg ...
        l = max(l, len(dd[0])) # handle long names
        names.append(dd[0])
        lengths.append(l)
    for col in range(len(lengths)):
        if rowlens:
            rls = [len(str(row[col])) for row in data if row[col]]
            lengths[col] = max([lengths[col]]+rls)
        rules.append("-"*lengths[col])
    format = " ".join(["%%-%ss" % l for l in lengths])
    result = [format % tuple(names)]
    result.append(format % tuple(rules))
    for row in data:
        result.append(format % tuple(row))
    return "\n".join(result)

def string_to_query(model_class, query_string):
    model = runtime.load_class(model_class)
    filter = model.objects
    #query_string = '{function_name}-{param_name}:{param_value}+{value};{function_name}-{param_name}:{param_value}'
    #query_string = 'filter-name:Digicel+3;exclude-name:Digicel'
    function_list = query_string.split(';')
    filter = None
    for function in function_list:
        full_function = function.split('-')
        func_name = full_function[0]
        params = full_function[1].split('+')
        
        param_dict = {}
        param_list = []
        for param in params:
            tmp = param.split(':')
            if len(tmp) == 2:
                param_dict[tmp[0]] = coerce_types.string_to_value(tmp[1])
            elif len(tmp) == 1:
                param_list.append(tmp[0])
            
        filter = queryset_query(filter, func_name, *param_list, **param_dict)
        
    return filter

def object_query(model_class, func_name, **kwargs):
    """
    Support for 'get', 'create', 'get_or_create' 
    """
    model = runtime.load_class(model_class)
    function = str_to_model_function(model, func_name)
    
    return function(**kwargs)

def queryset_query(filter, func_name, *arg, **kwargs):
    """
    Support for 'filter', 'exclude', 'annotate', 'order_by', 'reverse',
    'distinct', 'values', 'values_list', 'dates', 'none', 'all',
    'extra', 'defer', 'only'
    
    """
    function = str_to_query_function(filter, func_name)
    
    if len(arg) == 0 and len(kwargs) != 0:
        return function(**kwargs)
    if len(arg) != 0 and len(kwargs) == 0:
        return function(*arg)
    if len(arg) == 0 and len(kwargs) == 0:
        return function()
    if len(arg) != 0 and len(kwargs) != 0:
        return function(*arg, **kwargs)
    
    return None
    
def str_to_model_function(model, func_name):
    func_name = func_name.tolower()
    if func_name == 'get':
        return model.objects.get
    if func_name == 'create':
        return model.objects.create
    if func_name == 'get_or_create':
        return model.objects.get_or_create
    
    return None
    
def str_to_query_function(queryset, func_name):
    func_name = func_name.tolower()
    if func_name == 'filter':
        return queryset.filter
    if func_name == 'exclude':
        return queryset.exclude
    if func_name == 'annotate':
        return queryset.annotate
    if func_name == 'order_by':
        return queryset.order_by
    if func_name == 'reverse':
        return queryset.reverse
    if func_name == 'distinct':
        return queryset.distinct
    if func_name == 'values':
        return queryset.values
    if func_name == 'values_list':
        return queryset.values_list
    if func_name == 'dates':
        return queryset.dates
    if func_name == 'none':
        return queryset.none
    if func_name == 'all':
        return queryset.all
    if func_name == 'extra':
        return queryset.extra
    if func_name == 'defer':
        return queryset.defer
    if func_name == 'only':
        return queryset.only
    
    return None