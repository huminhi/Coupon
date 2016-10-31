
__all__ = [
        'Record',
        ]


from itertools import izip


class record(type):

    def __new__(meta, name, bases, bdict):
        slots = bdict['__slots__']
        if slots and '__init__' not in bdict:
            def __init__(self, *args, **kwargs):
                for (slot, value) in zip(slots, args):
                    setattr(self, slot, value)
                for kw in kwargs:
                    if kw in slots:
                        setattr(self, kw, kwargs[kw])
                    else:
                        raise Exception, 'Invalid slot: "%s"' % (kw,)
            bdict['__init__'] = __init__
        return super(record, meta).__new__(meta, name, bases, bdict)


class Record(object):
    __metaclass__ = record
    __slots__ = ()

    def __repr__(self):
        args = ', '.join( '%s=%r' % item for item in self._items() )
        return '%s(%s)' % (self.__class__.__name__, args)

    def __iter__(self):
        return ( getattr(self, s, None) for s in self.__slots__ )

    def _items(self):
        return izip(self.__slots__, self)


