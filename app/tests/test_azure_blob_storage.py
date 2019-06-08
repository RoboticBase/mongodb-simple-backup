import os

from src.azure_blob_storage import AzureBlobStorage


def test_upload(mocker):
    account_name = 'test_account_name'
    account_key = 'test_account_key'
    container_name = 'test_container_name'
    dump_dir = '/foo/bar'
    dump_file = 'test_dump_file'
    dump_path = os.path.join(dump_dir, dump_file)

    mocked_class = mocker.patch('src.azure_blob_storage.BlockBlobService')
    mocked_instance = mocker.Mock()
    mocked_class.return_value = mocked_instance

    azureBlobStorage = AzureBlobStorage(account_name, account_key)
    mocked_class.assert_called_once_with(account_name=account_name, account_key=account_key)

    azureBlobStorage.upload(container_name, dump_path)
    mocked_instance.create_blob_from_path.assert_called_once_with(container_name, dump_file, dump_path)
