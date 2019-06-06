#!/usr/bin/env python
import json
import logging.config
from logging import getLogger
import os

from src import const
from src.mongodb import MongoDB
from src.azure_blob_storage import AzureBlobStorage

mongodb_host = os.environ.get(const.MONGODB_HOST, '')
mongodb_port = os.environ.get(const.MONGODB_PORT, '')
account_name = os.environ.get(const.STORAGE_ACCOUNT, '')
account_key = os.environ.get(const.ACCOUNT_KEY, '')
container_name = os.environ.get(const.STORAGE_CONTAINER, '')

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
    dump_file = MongoDB(mongodb_host, mongodb_port).dump()
    azure_blob = AzureBlobStorage(account_name, account_key)
    azure_blob.upload(container_name, dump_file)
    logger.info('finish main')


if __name__ == '__main__':
    main()
