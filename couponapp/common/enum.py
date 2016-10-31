
__all__ = [
    'enum',
    'Enum',
    ]


class enum(type):

    def __new__(meta, name, bases, bdict):
        labels = []
        lindex = {}
        vindex = {}
        for (key, value) in bdict.items():
            if not key.isupper():
                continue
            if isinstance(value, tuple):
                (value, label) = value
            else:
                label = key.replace('_', ' ').title()
            labels.append( (value, label) )
            lindex[key] = value
            lindex[label] = value
            vindex[value] = (key, label)
        labels.sort()
        bdict['_labels'] = labels
        bdict['_label_index'] = lindex
        bdict['_value_index'] = vindex
        def get_name(value):
            return vindex[value][0]
        def get_label(value):
            return vindex[value][1]
        def get_value(name):
            return lindex[name]
        bdict['get_name'] = staticmethod(get_name)
        bdict['get_label'] = staticmethod(get_label)
        bdict['get_value'] = staticmethod(get_value)
        return super(enum, meta).__new__(meta, name, bases, bdict)


class Enum(object):
    __metaclass__ = enum


