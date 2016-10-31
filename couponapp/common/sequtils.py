

__all__ = [
        'pairs',
        'popwhile',
        ]


def pairs(seq):
    """\
    This returns an iterator over the pairs of items in a sequence. The last
    pair is the last element of the original sequence and None.

    >>> list(pairs(xrange(10)))
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, None)]

    """

    seq = iter(seq)
    prev = seq.next()
    while True:
        try:
            current = seq.next()
        except StopIteration:
            yield (prev, None)
            return
        else:
            yield (prev, current)
            prev = current


def popwhile(q, f):
    """\
    Takes a deque and a predicate function and returns all the left-hand items
    from the deque that return True when applied to f.

    """

    while len(q) > 0 and f(q[0]):
        yield q.popleft()



