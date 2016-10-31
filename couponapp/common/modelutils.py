
__all__ = [
    'EncryptedField',
    ]


import binascii
try:
    from cPickle import loads, dumps, HIGHEST_PROTOCOL
except ImportError:
    from pickle import loads, dumps, HIGHEST_PROTOCOL

from Crypto.Cipher import Blowfish


class EncryptedField(object):
    """\
    This uses a Blowfish from PyCrypto to encrypt the value stored in another
    field. The field should be a basic, picklable type: integer, string, or
    whatever.

    """

    def __init__(self, field_name, key=None):
        self.field_name = field_name
        if key is None:
            from django.conf import settings
            key = settings.SECRET_KEY
        self.key = key

    def __get__(self, instance, owner):
        cipher = Blowfish.new(self.key)
        encrypted = getattr(instance, self.field_name)
        if encrypted is None:
            return None
        if isinstance(encrypted, unicode):
            encrypted = encrypted.encode('utf-8')
        plain_text = cipher.decrypt(binascii.a2b_hex(encrypted)).rstrip()
        try:
            plain_obj = loads(plain_text)
        except:
            plain_obj = None
        return plain_obj

    def __set__(self, instance, value):
        if value is None:
            setattr(instance, self.field_name, None)
        else:
            cipher = Blowfish.new(self.key)
            plain_text = dumps(value, HIGHEST_PROTOCOL)
            padding = 8 - (len(plain_text) % 8)
            plain_text += ' ' * padding
            encrypted = binascii.b2a_hex(cipher.encrypt(plain_text))
            setattr(instance, self.field_name, unicode(encrypted))

    def __delete__(self, instance):
        setattr(instance, self.field_name, None)

