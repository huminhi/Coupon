

__all__ = [
        'clean_cc_number',
        'make_id_list',
        'safe_int',
        'get_int_param',
        'not_undefined',
        'cached_property',
        'is_int',
        'strip_diacritics',
        ]


from collections import deque
import re
from unicodedata import decomposition
from datetime import datetime

CLEAN_CC = re.compile(r'\d')


def clean_cc_number(cc_no, replace='#', leave=4):
    """\
    This sanitizes a credit card number by replacing all the digits except the
    trailing 'leave' digits with 'replace'.

    """

    return CLEAN_CC.sub(replace, cc_no[:-leave]) + cc_no[-leave:]


def make_id_list(data):
    """\
    This takes a string of database IDs, separated by pipes, and converts them
    to a list of int IDs.

    """

    ids = [ safe_int(did) for did in data.split('|') ]
    return [ i for i in ids if i is not None ]


def safe_int(val, default=None):
    try:
        return int(val)
    except:
        return default

def safe_float(val, default=None):
    try:
        return float(val)
    except:
        return default

def safe_bool(value, default=None):
    bool_value = default
    try:
        if(value.lower() == 'true'):
            bool_value = True
        elif(value.lower() == 'false'):
            bool_value = False
        else:
            bool_value = default
    except:
        bool_value = default
        
    return bool_value

def safe_datetime(value, default=None):
    dt_value = default
    try:
        'yyyy/MM/dd HH:mm:ss'
        dt_value = datetime(int(value[:4]), int(value[5:7]), int(value[8:10]), 
                            int(value[11:13]), int(value[14:16]), int(value[17:19]))
        
    except:
        dt_value = default
    
    return dt_value

def get_int_param(params, key, default=None):
    """\
    This looks in a parameter dict-like thing and returns key, if it is there
    and can be turned into an int. If it is missing or cannot, this returns
    default.

    """

    try:
        return safe_int(params[key])
    except:
        return default


def string_to_value(string_value):
    value = string_value
    if (string_value != None):
        value = safe_int(string_value)
        if value is None:
            value = safe_float(string_value)
            if value is None or ('.' not in string_value):
                value = safe_bool(string_value)
                if value is None:
                    value = safe_datetime(string_value)
                    if value is None:
                        value = string_value
    return value

def not_undefined(value):
    """ This returns None if value == 'undefined'. """
    return (value if value != u'undefined' else None)


class cached_property(object):
    """\
    This is a descriptor that implements a cached property.

    To use this, just pass it a function that produces a value and assign the
    result to a new object. If the function returns None, that isn't cached,
    and the function is attempted again the next time the property is called.

    For example, this defines two cached properties, one that will get cached,
    and one that never will::

    >>> class Cached(object):
    ...     def make_answer(self):
    ...         return 42
    ...     answer = cached_property(make_answer)
    ...     def make_nothing(self):
    ...         return None
    ...     nothing = cached_property(make_nothing)
    ...

    First, the 'answer' property is cached as '__make_answer' (the name of the
    producer thunk)::

    >>> cached = Cached()
    >>> hasattr(cached, '__make_answer')
    False
    >>> cached.answer
    42
    >>> hasattr(cached, '__make_answer')
    True

    But the 'nothing' property is never cached, because it always returns
    'None'::

    >>> hasattr(cached, '__make_nothing')
    False
    >>> print cached.nothing
    None
    >>> hasattr(cached, '__make_nothing')
    False

    Deleting a property clears the cache.

    >>> del cached.answer
    >>> hasattr(cached, '__make_answer')
    False

    """

    def __init__(self, producer, name=None, empty=None, doc=None):
        """\
        producer is the function that creates the value to cache.
        name is the name to store it under in the original object. If not
            given, the name of the producer, is used.
        doc is a documentation string.

        """

        self.producer = producer
        self.name = '__' + (name if name is not None else producer.__name__)
        self.empty = empty
        self.doc = doc

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.name, None)
        if value is None:
            value = self.producer(obj)
            if value != self.empty:
                setattr(obj, self.name, value)
        return value

    def __set__(self, obj, value):
        raise AttributeError, 'read-only attribute: ' + name

    def __delete__(self, obj):
        if hasattr(obj, self.name):
            delattr(obj, self.name)


def is_int(value):
    try:
        int(value)
    except:
        return False
    else:
        return True


def decompose(unistr):
    word = deque(unistr)
    buffer = []
    while len(word) > 0:
        char = word.popleft()
        decomp = decomposition(char)
        if decomp:
            decomp = [
                    unichr(int(x, 16)) for x in decomp.split() if x[0] != '<'
                    ]
            word.extendleft(reversed(decomp))
        else:
            buffer.append(char)
    return u''.join(buffer)


def strip_diacritics(value):
    if not isinstance(value, unicode):
        return value
    value = decompose(value)
    return u''.join( c for c in value if ord(c) < 256 )

def is_none_or_empty(param):
    result = True
    if param != '' and param != None:
        result = False
        
    return result
