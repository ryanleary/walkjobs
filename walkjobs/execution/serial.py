from walkjobs.execution.default import ExecutionStrategy, TaskStatus, TaskState
from multiprocessing import Process


class SerialTaskStatus(TaskStatus):
    __process = None

    def __init__(self, process):
        self.__process = process

    @property
    def state(self):
        if self.__process.is_alive():
            status = TaskState.RUNNING
        elif self.__process.exitcode is not None:
            status = TaskState.DONE
        else:
            status = TaskState.UNSTARTED
        return status

    def exitcode(self):
        return self.__process.exitcode


class SerialExecutionStrategy(ExecutionStrategy):
    def execute(self, f, args, kwargs):
        print 'Local exec:'
        print '  Function: ' + str(f)
        print '  Args: ' + str(args)
        print '  Kwargs: ' + str(kwargs)
        p = Process(target=f, args=args, kwargs=kwargs)
        p.start()
        p.join()
        return SerialTaskStatus(p)