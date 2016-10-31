

__all__ = [
        'serialize_graph',
        'deserialize_graph',
        ]


from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db.models import ForeignKey, ManyToManyField, OneToOneField


class model_list(list):
    __slots__ = ('seen',)

    def __init__(self):
        super(model_list, self).__init__()
        self.seen = set()

    def append_graph(self, obj):
        if obj is None:
            return
        ct = ContentType.objects.get_for_model(obj)
        key = ('%s.%s' % (ct.app_label, ct.model), obj.pk)
        if key not in self.seen:
            self.seen.add(key)
            self.append(obj)
            for f in obj._meta.fields:
                if isinstance(f, (ForeignKey, ManyToManyField, OneToOneField)):
                    self.append_graph(getattr(obj, f.name))


def make_graph(obj):
    graph = model_list()
    graph.append_graph(obj)
    graph.reverse()
    return list(graph)


def serialize_graph(obj, serializer, stream):
    """\
    This serializes an object model graph.

    The objects are serialized in reverse order of dependency. I.e., objects
    that are referenced by other objects are serialized first in the list.

    'serializer' is either a Django serializer or a string specifying the
    serialization format.

    'stream' is a file-like object for writing the serialized graph to.

    """

    if isinstance(serializer, basestring):
        sclass = serializers.get_serializer(serializer)
        serializer = sclass()
    serializer.serialize(make_graph(obj), stream=stream)


def deserialize_graph(format, stream):
    """\
    This deserializes an object model graph.

    The returned objects aren't standard Model subclass instances. See
    http://docs.djangoproject.com/en/dev/topics/serialization/#deserializing-data

    'format' is a string specifying the serialization format.

    'stream' is a file-like object for reading the serialized graph from.

    """

    data = stream.read()
    return list(serializers.deserialize(format, data))


