from job import Job, JobState
import logging
import time
import subprocess

logger = logging.getLogger(__name__)


class SgeJob(Job):
    def execute(self):
        logger.debug("Executing on SGE " + str(self))
        self._state = JobState.RUNNING
        subprocess.call(["ls", "-l"], stdout=open("/dev/null"))
        self.run()
        self._state = JobState.DONE