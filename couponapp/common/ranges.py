
__all__ = [
        'drange',
        'frange',
        'range_str_iter',
        'make_range_str',
        ]


from decimal import Decimal as D
from itertools import chain, imap


D0 = D(0)
D1 = D(1)


def frange(start, end=None, inc=None):
    """\
    A range clone for Decimals.

    This is modified slightly from http://code.activestate.com/recipes/66472/.

    """

    if end is None:
        end = start + 0.0
        start = 0.0
    if inc is None:
        inc = 1.0
    output = []
    while True:
        next = start + len(output) * inc
        if inc > 0.0 and next >= end:
            break
        elif inc < 0.0 and next <= end:
            break
        output.append(next)
    return output


def drange(start, end=None, inc=None):
    """\
    A range clone for Decimals.

    This is modified from http://code.activestate.com/recipes/66472/.

    """

    if end is None:
        end = start + D0
        start = D0
    if inc is None:
        inc = D1
    output = []
    while True:
        next = start + len(output) * inc
        if inc > D0 and next >= end:
            break
        elif inc < D0 and next <= end:
            break
        output.append(next)
    return output


def range_seq(rng):
    ends = [ e.strip() for e in rng.split('-') ]
    if len(ends) == 1:
        return [ int(ends[0]) ]
    else:
        return range(int(ends[0]), int(ends[1])+1)


def range_str_iter(ranges):
    """\
    This takes a series of ranges, separated by commas, and produces an
    iterator over those values.

    >>> list(range_str_iter("1, 2, 4, 6, 8-16, 24, 28-30"))
    [1, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 24, 28, 29, 30]

    """

    if not ranges.strip():
        return []
    return chain.from_iterable(imap(range_seq, ranges.split(',')))


def make_range_str(ints, sep=', '):
    """\
    This takes a sorted iterator of ints and returns a range string.

    >>> make_range_str([1, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 24, 28, 29, 30])
    '1-2, 4, 6, 8-16, 24, 28-30'

    """

    if not ints:
        return ''
    buffer = []
    start = None
    last = None
    for i in ints:
        if last is None:
            start = last = i
        elif i == last or i == (last + 1):
            last = i
        elif start == last:
            buffer.append(str(start))
            start = last = i
        else:
            buffer.append('%d-%d' % (start, last))
            start = last = i
    if start == last:
        buffer.append(str(start))
    else:
        buffer.append('%d-%d' % (start,last))
    return sep.join(buffer)


