from walkjobs.execution.default import ExecutionStrategy
import os
import drmaa
import logging

logger = logging.getLogger(__name__)


class GridExecutionStrategy(ExecutionStrategy):

    def __init__(self, queue=None):
        self._s = drmaa.Session()
        self._s.initialize()
        self._queue = queue

    def execute(self, f, args, kwargs):
        print 'Creating job template...'
        jt = self._s.createJobTemplate()
        jt.remoteCommand = os.getcwd() + '/sleeper.sh'
        jt.nativeSpecification = '-q all.q@@queuename'
        jt.args = ['42','Simon says:']
        jt.joinFiles = True

        jobid = self._s.runJob(jt)
        print 'Your job has been submitted with id ' + jobid
        self._s.control(jobid, drmaa.JobControlAction.HOLD)
        raw_input("Job held. Press Enter to release...")
        self._s.control(jobid, drmaa.JobControlAction.RELEASE)

        retval = self._s.wait(jobid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
        print 'Job: ' + str(retval.jobId) + ' finished with status ' + str(retval.hasExited)

        print jobid
        print retval

        print 'Cleaning up'
        self._s.deleteJobTemplate(jt)
        self._s.exit()

        print 'Grid exec: ' + str(f)
        pass