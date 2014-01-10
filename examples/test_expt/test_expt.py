import walkjobs
from walkjobs.execution import LocalExecutionStrategy
from external_programs import *


class AddJobOne(walkjobs.Job):
    def requires(self):
        pass

    def run(self):
        return [ExternalAdder(1, 2), Sleeper(20)]


class AddJobOnePointFive(walkjobs.Job):
    def requires(self):
        pass

    def run(self):
        return [ExternalAdder(187, 10), Sleeper(5), ExternalAdder(10, 12)]


class AddJobTwo(walkjobs.Job):
    def requires(self):
        return [AddJobOne, AddJobOnePointFive]

    def run(self):
        return [ExternalAdder(145, 10), ExternalAdder(12, 12)]


if __name__ == "__main__":
    walkjobs.run(verbosity=4, executor=LocalExecutionStrategy)