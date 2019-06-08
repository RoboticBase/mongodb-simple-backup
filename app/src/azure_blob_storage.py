from logging import getLogger
import os

from azure.storage.blob import BlockBlobService

logger = getLogger(__name__)


class AzureBlobStorage:
    def __init__(self, account_name, account_key):
        self.__block_blob_service = BlockBlobService(account_name=account_name,
                                                     account_key=account_key)

    def upload(self, container_name, file_path):
        logger.info(f'start upload, container={container_name}, file={file_path}')
        result = self.__block_blob_service.create_blob_from_path(
            container_name, os.path.basename(file_path), file_path)
        logger.info(f'finish upload, last_modified={result.last_modified}')
