import unittest
from walkjobs.execution import GridExecutionStrategy


class ExecutionTestCases(unittest.TestCase):
    def setUp(self):
        pass

    def test_sge(self):
        job = {}
        job.executor(GridExecutionStrategy())
        pass

if __name__ == '__main__':
    unittest.main()
