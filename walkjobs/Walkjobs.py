import logging
import argparse

from scheduler import scheduler
from execution import LocalExecutionStrategy
from job import RegisteredJob


logger = logging.getLogger(__name__)


class Walkjobs(object):

    def __init__(self, executor):
        logger.debug("Initializing Walkjobs")
        self._scheduler = scheduler.LocalScheduler(executor)
        self._jobs = RegisteredJob.get_registry()
        self._executor = executor

        for cls in self._jobs.itervalues():
            self._scheduler.add_job(cls)

    def start_execution(self):
        logger.info("Validating pipeline")
        self._scheduler.check_valid()
        logger.info("Executing pipeline")
        self._scheduler.execute()


    @classmethod
    def run(cls, verbosity=0, log_target=None, executor=LocalExecutionStrategy):
        configure_logging(verbosity, log_target)
        wj = Walkjobs(executor)
        wj.start_execution()


def configure_logging(verbosity=0, log_target=None):
    def get_level(v):
        return {0: logging.NOTSET,
                1: logging.CRITICAL,
                2: logging.ERROR,
                3: logging.WARNING,
                4: logging.INFO,
                5: logging.DEBUG}\
            .get(v, logging.NOTSET)
    # create logger
    lgr = logging.getLogger('walkjobs')
    lgr.setLevel(get_level(verbosity))
    # add a file handler
    fh = logging.StreamHandler()
    if log_target:
        fh = logging.StreamHandler(log_target)
    fh.setLevel(logging.DEBUG)
    # create a formatter and set the formatter for the handler.
    frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(frmt)
    # add the Handler to the logger
    lgr.addHandler(fh)
