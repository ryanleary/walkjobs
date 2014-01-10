from abc import abstractproperty
import os


class ExecutionStrategy(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout
        self._stderr = stderr

    def execute(self, cmd, *args, **kwargs):
        raise NotImplementedError('Must use Concrete Execution Strategy')


class TaskState(object):
    UNSTARTED = ("unstarted", "Not done")
    UNBLOCKED = ("unblocked", "Ready")
    QUEUED = ("queued", "Queued")
    RUNNING = ("running", "Running")
    FAILED = ("failed", "Failed")
    DONE = ("done", "Done")


class TaskStatus(object):
    @abstractproperty
    def state(self):
        return TaskState.UNSTARTED

    @abstractproperty
    def exitcode(self):
        return None


class Task(object):
    stdout = None
    stderr = None

    def __init__(self, *args, **kwargs):
        self._executor = ExecutionStrategy()
        self._args = args
        self._kwargs = kwargs
        self._status = TaskStatus()
        pass

    def set_executor(self, executor):
        self._executor = executor(stdout=self.stdout, stderr=self.stderr)

    def execute(self):
        self._status = self._executor.execute(self.cmd, *self._args, **self._kwargs)

    def wait(self):
        self._status.wait()

    @property
    def status(self):
        return self._status


class LocalTarget(object):
    is_open = False

    def __init__(self, filename, ephemeral=False):
        self._filename = filename
        self._ephemeral = ephemeral

    def to_write(self):
        if not self.is_open:
            self.is_open = True
            return open(self._filename, 'w')

    def to_read(self):
        if not self.is_open:
            self.is_open = True
            return open(self._filename, 'r')

    def get(self):
        f = self.to_read()
        data = f.read()
        f.close()
        if self._ephemeral:
            os.remove(self._filename)
        return data