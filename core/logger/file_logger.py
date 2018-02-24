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
from core.utils.environ import get_log_dir_path

from core.constants import LOG_FORMAT, central_logger_settings
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


def get_central_logger():
    central_logger = logging.getLogger("central_log")
    central_logger.setLevel(central_logger_settings['LOG_LEVEL'])

    handler = RotatingFileHandler(
        os.path.join(get_log_dir_path(), central_logger_settings['LOG_FILE_NAME']),
        maxBytes=central_logger_settings['LOG_FILE_MAX_BYTES'],
        backupCount=central_logger_settings['LOG_FILE_BACKUP_COUNT']
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    central_logger.addHandler(handler)

    return central_logger


central_logger = get_central_logger()


def central_logger_api(data, error=None):

    if error:
        central_logger.error('Error when received {}, {}'.format(data, error))

    elif not isinstance(data, dict):
        central_logger.info(data)

    else:
        _logger_obj = getattr(central_logger, data.get('loglevel', ''), '')

        _logger_obj = _logger_obj if _logger_obj else getattr(central_logger, 'info')

        _logger_obj(data)

