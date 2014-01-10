from walkjobs.execution.default import ExecutionStrategy


class GridExecutionStrategy(ExecutionStrategy):
    def execute(self, f, args, kwargs):
        print 'Grid exec: ' + str(f)
        pass