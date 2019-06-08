import datetime
from logging import getLogger
import os
import subprocess
import tarfile

from src import const


logger = getLogger(__name__)


class MongoDB:
    def __init__(self, endpoint, store_oplog):
        self.__endpoint = endpoint
        self.__store_oplog = store_oplog

    def dump(self, dumpfile_prefix, tz):
        logger.info(f'start dump, endpoint={self.__endpoint}, store_oplog={self.__store_oplog}')
        dump_dir = self.__get_dump_dir(dumpfile_prefix, tz)
        logger.info(f'exec dump command, dump_dir={dump_dir}')
        self.__exec_dump_cmd(dump_dir)
        logger.info(f'compress dump dir, dump_dir={dump_dir}')
        dump_file = self.__compress(dump_dir)
        logger.info(f'finish dump, dump_file={dump_file}')
        return dump_file

    def __get_dump_dir(self, dumpfile_prefix, tz):
        dt = datetime.datetime.now(tz=tz).strftime('%Y%m%d%H%M%S%Z')
        return os.path.join(const.DEFAULT_DUMPFILE_DIR, f'{dumpfile_prefix}{dt}')

    def __exec_dump_cmd(self, dump_dir):
        cmd = f'mongodump --host="{self.__endpoint}" --out="{dump_dir}"'
        if self.__store_oplog:
            cmd += ' --oplog'
        logger.info(f'dump command="{cmd}"')
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
