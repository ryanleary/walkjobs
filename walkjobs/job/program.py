import logging

logger = logging.getLogger(__name__)


class RegisteredJob(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        cls = super(mcs, RegisteredJob).__new__(mcs, name, bases, attrs)
        if name not in {'Job', 'SgeJob'}:
            mcs._registry[name] = cls
        return cls

    @classmethod
    def get_registry(mcs):
        return mcs._registry


class Job(object):
    __metaclass__ = RegisteredJob

    def __init__(self):
        self._state = JobState.UNSTARTED

    def is_complete(self):
        return self._state == JobState.DONE

    def requires(self):
        pass

    def execute(self):
        logger.debug("Executing " + str(self))
        self._state = JobState.RUNNING
        self.run()
        self._state = JobState.DONE

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