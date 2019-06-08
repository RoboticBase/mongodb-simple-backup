import datetime
from logging import getLogger
import os
import subprocess
import tarfile

import pytz

from src import const

dumpfile_prefix = os.environ.get(const.DUMPFILE_PREFIX, const.DEFAULT_DUMPFILE_PREFIX)
tzstr = os.environ.get(const.TIMEZONE, const.DEFAULT_TIMEZONE)
tz = pytz.timezone(tzstr)

logger = getLogger(__name__)


class MongoDB:
    def __init__(self, endpoint):
        self.__endpoint = endpoint

    def dump(self):
        logger.info(f'start dump, endpoint={self.__endpoint}')
        dump_dir = self.__get_dump_dir()
        logger.info(f'exec dump command, dump_dir={dump_dir}')
        self.__exec_dump_cmd(dump_dir)
        logger.info(f'compress dump dir, dump_dir={dump_dir}')
        dump_file = self.__compress(dump_dir)
        logger.info(f'finish dump, dump_file={dump_file}')
        return dump_file

    def __get_dump_dir(self):
        dt = datetime.datetime.now(tz=tz).strftime('%Y%m%d%H%M%S%Z')
        return os.path.join(const.DEFAULT_DUMPFILE_DIR, f'{dumpfile_prefix}{dt}')

    def __exec_dump_cmd(self, dump_dir):
        cmd = f'mongodump --host="{self.__endpoint}" --out="{dump_dir}" --oplog'
        proc = subprocess.run(cmd.split(),
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        logger.info(proc.stdout.decode('utf8'))
        logger.info(proc.stderr.decode('utf8'))

    def __compress(self, dump_dir):
        dump_file = f'{dump_dir}.tar.gz'
        with tarfile.open(dump_file, 'w|gz') as tar:
            tar.add(dump_dir, arcname=os.path.basename(dump_dir))

        return dump_file
