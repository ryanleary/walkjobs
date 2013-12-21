from scheduler import scheduler
from scheduler.job import RegisteredJob
import logging

logger = logging.getLogger(__name__)

class Walkjobs(object):

    def __init__(self):
        logger.debug("Initializing Walkjobs")
        self._scheduler = scheduler.LocalScheduler()
        self._jobs = RegisteredJob.get_registry()

        for cls in self._jobs.itervalues():
            self._scheduler.add_job(cls)

    def start_execution(self):
        logger.debug("Validating pipeline")
        self._scheduler.check_valid()
        logger.debug("Executing pipeline")
        self._scheduler.execute()


    @classmethod
    def run(cls, debug=None):
        if debug:
            enable_debug()
        wj = Walkjobs()
        wj.start_execution()


def enable_debug():
    # create logger
    lgr = logging.getLogger('walkjobs')
    lgr.setLevel(logging.DEBUG)
    # add a file handler
    fh = logging.StreamHandler()
    fh.setLevel(logging.DEBUG)
    # create a formatter and set the formatter for the handler.
    frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(frmt)
    # add the Handler to the logger
    lgr.addHandler(fh)