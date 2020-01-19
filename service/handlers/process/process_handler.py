from subprocess import Popen, PIPE
import logging

logger = logging.getLogger(__name__)


class Executor(object):
    def __init__(self):
        pass

    @staticmethod
    def execute(cmd):
        if not isinstance(cmd, list):
            cmd = [cmd]
        logger.info(f"Executing command: {cmd}")
        with Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True) as process:
            stdout = process.stdout.read().decode('utf-8')
            stderr = process.stderr.read().decode('utf-8')
        logger.debug("Command completed!")
        if len(stderr) > 0:
            raise RuntimeError(f"Process executor has exited with errors: {stderr}")
