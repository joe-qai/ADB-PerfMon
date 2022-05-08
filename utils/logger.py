# -*- coding: utf-8 -*-

from functools import wraps
import os

import logbook
from logbook.more import ColorizedStderrHandler

from adb.configpath import LOG_DIR


__author__ = "joe-tester"


def get_logger(name='adb_monkey_log', level="INFO"):
    """ get logger Factory function """
    logbook.set_datetime_format('local')
    ColorizedStderrHandler(bubble=False, level=level).push_thread()
    logbook.TimedRotatingFileHandler(
        os.path.join(LOG_DIR, '%s.log' % name),
        date_format='%Y-%m-%d-%H', bubble=True, encoding='utf-8',format_string="").push_thread()
    return logbook.Logger(name)

LOG = get_logger()

def logger(param):
    """ fcuntion from logger meta """
    def wrap(function):
        """ logger wrapper """
        @wraps(function)
        def _wrap(*args, **kwargs):
            """ wrap tool """
            LOG.info("Current module:{}".format(param))
            LOG.info("All args parameter information: {}".format(str(args)))
            LOG.info("All kwargs parameter information: {}".format(str(kwargs)))
            return function(*args, **kwargs)
        return _wrap
    return wrap