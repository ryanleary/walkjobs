from walkjobs.execution.default import ExecutionStrategy, TaskStatus, TaskState
from multiprocessing import Process
import subprocess
import logging

logger = logging.getLogger(__name__)


class LocalTaskState(TaskStatus):
    __process = None

    def __init__(self, process):
        super(TaskStatus, self).__init__()
        self.__process = process

    @property
    def state(self):
        if self.__process is None:
            return TaskState.UNSTARTED

        if self.__process.is_alive():
            status = TaskState.RUNNING
        elif self.__process.exitcode is not None:
            status = TaskState.DONE
        else:
            status = TaskState.UNSTARTED
        return status

    @property
    def exitcode(self):
        return self.__process.exitcode

    def wait(self):
        self.__process.join()


def do_task(cmd, stdout=None, stderr=None):
    if stdout is not None:
        stdout = stdout.to_write()
    if stderr is not None:
        stderr = stderr.to_write()
    subprocess.call(cmd, stdout=stdout, stderr=stderr)


class LocalExecutionStrategy(ExecutionStrategy):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout
        self._stderr = stderr

    def execute(self, cmd, *args, **kwargs):
        logger.debug('Local exec:')
        logger.debug('  Function: ' + str(cmd))
        logger.debug('  Args: ' + str(args))
        logger.debug('  Kwargs: ' + str(kwargs))
        logger.debug('  stdout: ' + str(self._stdout))
        logger.debug('  stderr: ' + str(self._stderr))
        p = Process(target=do_task,
                    args=(cmd(*args, **kwargs),),
                    kwargs={'stdout': self._stdout, 'stderr': self._stderr})
        p.start()
        return LocalTaskState(p)