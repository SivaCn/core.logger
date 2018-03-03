# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import os
import logging
import simplejson as json

from logging.handlers import RotatingFileHandler
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.environ import (
    get_log_dir_path, get_log_file_details
)

from core.constants import LOG_FORMAT, central_logger_settings
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


LOG_FILES = get_log_file_details()


def get_central_logger(category='default'):

    central_logger = logging.getLogger(category)

    central_logger.setLevel(central_logger_settings['LOG_LEVEL'])

    handler = RotatingFileHandler(
        os.path.join(get_log_dir_path(), LOG_FILES[category]),
        maxBytes=central_logger_settings['LOG_FILE_MAX_BYTES'],
        backupCount=central_logger_settings['LOG_FILE_BACKUP_COUNT']
    )

    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    central_logger.addHandler(handler)

    return central_logger


#
# XXX: This must be present here. Do not Remove.
LOGGERS = {
    'default': get_central_logger('default'),

    'process': get_central_logger('process'),
    'scheduler_svc': get_central_logger('scheduler_svc'),
    'scheduler_access': get_central_logger('scheduler_access'),

    'program_errors': get_central_logger('program_errors'),
}


def central_logger_api(data, error=None):

    if error:
        LOGGERS['program_errors'].error('Error when received {}, {}'.format(data, error))

    elif not isinstance(data, dict):
        LOGGERS['default'].info(data)

    else:

        log_category = data.pop('category', 'default')

        logger = LOGGERS.get(log_category)

        log_level = data.pop('log_level', 'info')

        _logger_obj = getattr(logger, log_level, None) or logger.info

        _logger_obj(data)

