

"""\
This sets up and provides logging functions.

This module is just a wrapper over the logging module in the standard
distribution, initialized from settings in the DJANGO_SETTINGS_MODULE.

To specify how to set up logging, use these settings in the
DJANGO_SETTINGS_MODULE:

LOGGING_OUTPUT:
    Where to send the logging output. This can be a file name, "-" or "STDOUT"
    (for outputting to STDOUT) or "STDERR" (for outputting to STDERR).

LOGGING_LEVEL:
    This is the logging level. This can be a value from the logging module or
    it can be a string naming such a value (e.g., "INFO" or "CRITICAL").

LOGGING_FORMAT:
    This is the logging format. By default this uses
    'lunex.log.DEFAULT_LOGGING_FORMAT'.

LOGGING_CONF:
    The absolute path to a logging configuration file, as described in
    http://docs.python.org/library/logging.html#configuring-logging.

    If given, this overrides all of the other settings.

If neither LOGGING_OUTPUT nor LOGGING_CONF are specified, logging.basicConfig
is called with all defaults.

This sets up a logger (stored in 'logger') with the name "lunex". You can
access this directly using the shortcut functions 'debug', 'info', 'warning',
'error', and 'critical'.

"""


__all__ = [
    'logger',
    'log',
    'debug',
    'info',
    'warning',
    'error',
    'exception',
    'critical',
    'setup_logger',
    ]


import atexit
import logging
import logging.config
import sys


DEFAULT_LOGGER_NAME = 'lunex'
DEFAULT_LOGGING_FORMAT = '%(asctime)s [%(name)s/%(levelname)s] %(message)s'
DEFAULT_MAX_BYTE = 200000000
DEFAULT_BACKUP_COUNT = 10

atexit.register(logging.shutdown)


def setup_logger(name):
    """\
    This sets up a logger with the given name, from the settings in
    DJANGO_SETTINGS_MODULE.

    """

    from django.conf import settings
    if hasattr(settings, 'LOGGING_CONF'):
        logging.config.fileConfig(settings.LOGGING_CONF)
        logger = logging.getLogger(name)
    elif hasattr(settings, 'LOGGING_OUTPUT'):
        # level
        level = getattr(settings, 'LOGGING_LEVEL')
        if isinstance(level, basestring):
            level = getattr(logging, str(level))
        # formatting
        format = getattr(settings, 'LOGGING_FORMAT', DEFAULT_LOGGING_FORMAT)
        formatter = logging.Formatter(format)
        # handler
        output = settings.LOGGING_OUTPUT
        if output == '-' or output == 'STDOUT':
            handler = logging.StreamHandler(sys.stdout)
        elif output == 'STDERR':
            handler = logging.StreamHandler(sys.stderr)
        elif getattr(settings, 'LOGGING_FILEROTATION', False):
            max_byte = getattr(settings, 'LOGGING_MAXBYTE', DEFAULT_MAX_BYTE)
            backup_count = getattr(settings, 'LOGGING_BACKUP_COUNT', DEFAULT_BACKUP_COUNT)
            handler = logging.handlers.RotatingFileHandler(output, 'a', max_byte, backup_count)
        else:
            handler = logging.FileHandler(output)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        # logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
    else:
        logging.basicConfig()
        logger = logging.getLogger(name)
    return logger


try:
    logger
except:
    logger = setup_logger(DEFAULT_LOGGER_NAME)


def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    logger.exception(msg, *args, **kwargs)


def log(level, msg, *args, **kwargs):
    logger.log(level, msg, *args, **kwargs)



