

__all__ = [
        'file_lock',
        'open_file',
        ]


from contextlib import contextmanager
import logging
import sys

from lunex.common.pathutils import Lock, LockError


@contextmanager
def file_lock(lock_file):
    """\
    This locks a file and returns True or False whether the lock succeeded.

    """

    lock = Lock(lock_file)
    try:
        lock.lock(False)
    except LockError:
        is_locked = False
    else:
        is_locked = True
    try:
        yield is_locked
    finally:
        if is_locked:
            lock.unlock()


@contextmanager
def open_file(filename, mode='w'):
    close = False
    if 'w' in mode or 'a' in mode:
        if filename in (None, '-', 'STDOUT'):
            logging.info('writing output to STDOUT')
            f = sys.stdout
        elif filename == 'STDERR':
            logging.info('writing output to STDERR')
            f = sys.stderr
        elif isinstance(filename, basestring):
            logging.info('writing output to "%s"', filename)
            f = open(filename, mode)
            close = True
        else:
            logging.info('writing output to file-like object %r', filename)
            f = filename
    elif 'r' in mode:
        if filename in (None, '-', 'STDIN'):
            logging.info('reading input from STDIN')
            f = sys.stdin
        elif isinstance(filename, basestring):
            logging.info('reading input from "%s"', filename)
            f = open(filename, mode)
            close = True
        else:
            logging.info('reading input from file-like object %r', filename)
            f = filename
    else:
        logging.info('opening "%s" with mode "%s"', filename, mode)
        f = open(filename, mode)
        close = True
    try:
        yield f
    finally:
        if close:
            f.close()


