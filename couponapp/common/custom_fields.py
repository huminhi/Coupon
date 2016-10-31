#from django.db.models.fields import IntegerField
#
#__all__ = [
#        'BigIntegerField',
#        ]
#
## Quick hack from
## http://www.mattwaite.com/posts/2009/mar/10/django-and-really-big-numbers/
#class BigIntegerField(IntegerField):
#    """\
#    Analogous to django.db.models.fields.IntegerField except that it creates
#    a bigint in the database instead of an integer.
#    """
#    
#    empty_strings_allowed=False
#    def get_internal_type(self):
#        return "BigIntegerField"    
#    def db_type(self):
#        return 'bigint' # Note this won't work with Oracle.
#    
#    