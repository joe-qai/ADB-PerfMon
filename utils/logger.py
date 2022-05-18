# -*- coding: utf-8 -*-

from functools import wraps
import os
import logbook
import logbook.more

from common.configpath import LOG_DIR

__author__ = "joe-tester"


def logFormate(record, handler):
    """Log format"""
    # record.to_dict()
    formate = "[{date}] [{level}] [{filename}] [{func_name}] [{lineno}] {msg}".format(
        date=record.time,
        level=record.level_name,
        filename=os.path.split(record.filename)[-1],
        func_name=record.func_name,
        lineno=record.lineno,
        msg=record.message
    )
    return formate


def get_logger(name='adb_monkey_log', fileLogFlag=True, stdOutFlag=False, level="INFO"):
    """ get logger Factory function """
    logbook.set_datetime_format('local')
    logger = logbook.Logger(name)
    logger.handlers = []
    if fileLogFlag:
        logFile = logbook.TimedRotatingFileHandler(os.path.join(LOG_DIR, '%s.log' % name), date_format='%Y-%m-%d-%H',
                                                   bubble=True, encoding='utf-8')  # .push_thread()
        logFile.formatter = logFormate
        logger.handlers.append(logFile)
    if stdOutFlag:
        logStd = logbook.more.ColorizedStderrHandler(bubble=True)
        logStd.formatter = logFormate
        logger.handlers.append(logStd)
    return logger


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