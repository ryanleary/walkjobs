import logging
from threading import Thread

logger = logging.getLogger(__name__)


class RegisteredJob(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        cls = super(mcs, RegisteredJob).__new__(mcs, name, bases, attrs)
        if name not in {'Job'}:
            mcs._registry[name] = cls
        return cls

    @classmethod
    def get_registry(mcs):
        return mcs._registry


class Job(object):
    __metaclass__ = RegisteredJob

    def __init__(self, executor):
        self._state = JobState.UNSTARTED
        self._executor = executor

    def is_complete(self):
        return self._state == JobState.DONE

    def requires(self):
        pass

    def __do_execute(self):
        self._state = JobState.RUNNING
        tasks = self.run()
        for task in tasks:
            task.set_executor(self._executor)
            task.execute()
            task.wait()
        self._state = JobState.DONE

    def execute(self):
        logger.info("Spawning thread to execute tasks in " + str(self))
        t = Thread(target=self.__do_execute)
        t.start()

    def get_state(self):
        return self._state

    def queue(self):
        self._state = JobState.QUEUED

    @classmethod
    def __str__(cls):
        return cls.__name__

    @classmethod
    def __repr__(cls):
        return cls.__str__()

    def run(self):
        pass


class JobState(object):
    UNSTARTED = ("unstarted", "Not done")
    UNBLOCKED = ("unblocked", "Ready")
    QUEUED = ("queued", "Queued")
    RUNNING = ("running", "Running")
    FAILED = ("failed", "Failed")
    DONE = ("done", "Done")