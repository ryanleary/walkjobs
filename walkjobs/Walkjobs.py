from scheduler import scheduler
from scheduler.job import RegisteredJob


class Walkjobs(object):

    def __init__(self):
        self._scheduler = scheduler.LocalScheduler()
        self._jobs = RegisteredJob.get_registry()

        for cls in self._jobs.itervalues():
            self._scheduler.add_job(cls)

    def start_execution(self):
        self._scheduler.check_valid()
        self._scheduler.execute()


    @classmethod
    def run(cls):
        wj = Walkjobs()
        wj.start_execution()