import os
from subprocess import PIPE

import pytest
import pytz

from src.mongodb import MongoDB, const


@pytest.mark.parametrize('store_oplog', [True, False])
@pytest.mark.freeze_time('2018-01-02T03:04:05+09:00')
def test_get_dump_dir(mocker, store_oplog):
    endpoint = 'endpoint'
    dumpfile_prefix = 'test_'
    tz = pytz.timezone('Asia/Tokyo')

    base_dir = f'{dumpfile_prefix}20180102030405JST'
    dump_dir = os.path.join(const.DEFAULT_DUMPFILE_DIR, base_dir)
    dump_file = f'{dump_dir}.tar.gz'

    mocked_subprocessrun = mocker.patch('subprocess.run')
    mocked_tarfileopen = mocker.patch('tarfile.open')
    mocked_tar = mocker.Mock()
    mocked_tarfileopen.return_value.__enter__.return_value = mocked_tar

    result = MongoDB(endpoint, store_oplog).dump(dumpfile_prefix, tz)

    if store_oplog:
        mocked_subprocessrun.assert_called_once_with(
            ['mongodump', f'--host="{endpoint}"', f'--out="{dump_dir}"', '--oplog'],
            stdout=PIPE,
            stderr=PIPE)
    else:
        mocked_subprocessrun.assert_called_once_with(
            ['mongodump', f'--host="{endpoint}"', f'--out="{dump_dir}"'],
            stdout=PIPE,
            stderr=PIPE)
    mocked_tarfileopen.assert_called_once_with(dump_file, 'w|gz')
    mocked_tar.add.assert_called_once_with(dump_dir, arcname=base_dir)

    assert result == dump_file
