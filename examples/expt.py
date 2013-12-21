import walkjobs
import logging

class SimulJobOne(walkjobs.Job):
    def requires(self):
        pass

    def run(self):
        print "job1a"


class SimulJobTwo(walkjobs.Job):
    def requires(self):
        pass

    def run(self):
        print "job1b"


class JobThree(walkjobs.Job):
    def requires(self):
        return [SimulJobOne, SimulJobTwo]

    def run(self):
        print "job3"


class JobFourA(walkjobs.SgeJob):
    def requires(self):
        return [JobThree]

    def run(self):
        print "job4a"


class JobFourB(walkjobs.Job):
    def requires(self):
        return [JobThree]

    def run(self):
        print "job4b"


if __name__ == "__main__":
    walkjobs.run(debug=True)