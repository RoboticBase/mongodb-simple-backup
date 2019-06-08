#!/usr/bin/env python
import distutils.util
import json
import logging.config
from logging import getLogger
import os

import pytz

from src import const
from src.mongodb import MongoDB
from src.azure_blob_storage import AzureBlobStorage


try:
    with open(const.LOGGING_JSON, "r") as f:
        logging.config.dictConfig(json.load(f))
        if (const.LOG_LEVEL in os.environ and
                os.environ[const.LOG_LEVEL].upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
            for handler in getLogger().handlers:
                if handler.get_name() in const.TARGET_HANDLERS:
                    handler.setLevel(getattr(logging, os.environ[const.LOG_LEVEL].upper()))
except FileNotFoundError:
    print(f'can not open {const.LOGGING_JSON}')
    pass

logger = getLogger(__name__)


def main():
    logger.info('start main')

    try:
        mongodb_endpoint = os.environ[const.MONGODB_ENDPOINT]
        account_name = os.environ[const.STORAGE_ACCOUNT]
        account_key = os.environ[const.ACCOUNT_KEY]
        container_name = os.environ[const.STORAGE_CONTAINER]
        store_oplog = bool(distutils.util.strtobool(os.environ.get(const.STORE_OPLOG, const.DEFAULT_STORE_OPLOG)))
        dumpfile_prefix = os.environ.get(const.DUMPFILE_PREFIX, const.DEFAULT_DUMPFILE_PREFIX)
        tzstr = os.environ.get(const.TIMEZONE, const.DEFAULT_TIMEZONE)
    except (KeyError, ValueError) as e:
        logger.exception(e)
        exit(1)

    try:
        tz = pytz.timezone(tzstr)

        dump_file = MongoDB(mongodb_endpoint, store_oplog).dump(dumpfile_prefix, tz)
        AzureBlobStorage(account_name, account_key).upload(container_name, dump_file)
    except Exception as e:
        logger.exception(e)
        exit(1)

    logger.info('finish main')


if __name__ == '__main__':
    main()
