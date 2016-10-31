

"""\
This contains template tags and filters for working with Lunex data.

"""


from decimal import Decimal
import sys
import time
import traceback
import locale

from django import template
from django.forms import CheckboxInput, RadioSelect, CheckboxSelectMultiple

from lunex.common.coerce_types import clean_cc_number
from lunex.common.users import get_name

register = template.Library()


D1_00 = Decimal('1.00')
MAX_TRIES = 3

def format_number(val,decimal_places = 2):
    return "$"+locale.format("%0.{0}f".format(decimal_places), val, grouping=True)

def formatCurrency(val,decimal_places = 2):
    try:
        if val == None:
            return None;
        
        if val < 0:
            txt = '(%s)' % format_number(-val,decimal_places);
        else:
            txt = format_number(val,decimal_places);
        return txt;
    except Exception:
        return val;

@register.filter(name="currency")
def currency(val):
    return formatCurrency(val);

@register.filter(name='moneyfmt')
def moneyfmt(value, places=2, curr='', sep=',', dp='.', pos='', neg='-', trailneg='', q=D1_00):
    """\
    This is a brain-dead, template-ready version of the moneyfmt function
    in the Python documentation (http://docs.python.org/library/decimal.html).

    """

    try:
        if value is None:
            return '0.00'
        elif isinstance(value, basestring):
            return value
        elif isinstance(value, float):
            value = Decimal(str(value))
        if q is None:
            q = Decimal(10) ** -places
        # TODO need to track down the root of the quantize error better
        try:
            value = value.quantize(q)
        except:
            value = str(value)
            i = value.find('.')
            if i == -1:
                return value
            else:
                return value[:i+places+1]
        (sign, digits, exp) = value.as_tuple()
        result = []
        digits = map(str, digits)
        (build, next) = (result.append, digits.pop)
        if sign:
            build(trailneg)
        for i in range(places):
            build(next() if digits else '0')
        build(dp)
        if not digits:
            build('0')
        i = 0
        while digits:
            build(next())
            i += 1
            if i == 3 and digits:
        	i = 0
        	build(sep)
        build(curr)
        build(neg if sign else pos)
        return ''.join(reversed(result))
    except:
        traceback.print_exc(file=sys.stderr)
        raise


@register.filter(name='percentfmt')
def percentfmt(value, offset=2, places=2, perc='', sep=',', dp='.', pos='', neg='-', trailneg=''):
    """\
    This formats a Decimal as if it were a percent. It multiplies it by 100 and
    formats it similar to moneyfmt.

    """

    if value is None:
        return ''
    elif isinstance(value, basestring):
        return value
    elif isinstance(value, float):
        fmt = '%.' + str(places) + 'f'
        return fmt % (value * (10**offset),)
    q = Decimal(10) ** -(offset+places)
    try:
        value = value.quantize(q)
    except:
        value = str(value)
        i = value.find('.')
        if i == -1:
            return value
        else:
            return value[:i+places+1]
    (sign, digits, exp) = value.as_tuple()
    result = []
    digits = map(str, digits)
    (build, next) = (result.append, digits.pop)
    build(perc)
    if sign:
        build(trailneg)
    for i in range(places):
        build( next() if digits else '0' )
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build( neg if sign else pos )
    return ''.join(reversed(result))


register.filter(name='cc_safe')(clean_cc_number)


@register.filter(name='name')
def name(user):
    if not user: return None
    elif hasattr(user, 'user'): return name(user.user)
    else: return get_name(user)


@register.filter(name='xmlcharref')
def xmlcharref(value):
    if isinstance(value, unicode):
        return value.encode('ascii', 'xmlcharrefreplace')
    else:
        return value


@register.filter(name='as_phone_no')
def as_phone_number(numbers):
    """\
    This takes a sequence of numbers and puts parentheses around the area code
    and a dash between the prefix and the rest of the number.

    >>> as_phone_number('1234567')
    u'123-4567'
    >>> as_phone_number('1234567890')
    u'(123)456-7890'
    >>> as_phone_number('11234567890')
    u'1-(123)456-7890'
    >>> as_phone_number('1234567890123')
    u'1234567890123'

    """

    number_count = len(numbers)
    if number_count == 7:
        return u'%s-%s' % (numbers[:3], numbers[3:])
    elif number_count == 10:
        return u'(%s)%s-%s' % (numbers[:3], numbers[3:6], numbers[6:])
    elif number_count == 11:
        return u'%s-(%s)%s-%s' % (numbers[0], numbers[1:4], numbers[4:7],
                                  numbers[7:])
    else:
        return unicode(numbers)


@register.filter(name='is_neg')
def is_neg(value):
    """ This returns True if value < 0. """
    return value < 0


@register.filter(name='truncatechars')
def truncatechars(value, chars='25'):
    value = unicode(value)
    chars = int(chars)
    if len(value) <= chars:
        return value
    return value[:chars] + u'...'


@register.filter(name='truncateleft')
def truncateleft(value, chars='25'):
    value = unicode(value)
    chars = int(chars)
    if len(value) <= chars:
        return value
    return u'...' + value[-chars:]


@register.inclusion_tag('lunex/left_field.html')
def left_field(field):
    return {
            'field': field,
            'is_choice': isinstance(field.field.widget,
                (CheckboxInput, RadioSelect, CheckboxSelectMultiple)),
        }


@register.inclusion_tag('lunex/form_field.html')
def form_field(field):
    return {
            'field': field,
            'is_choice': isinstance(field.field.widget,
                (CheckboxInput, RadioSelect, CheckboxSelectMultiple)),
            }


if __name__ == '__main__':
    import doctest
    doctest.testmod()

