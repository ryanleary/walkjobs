from walkjobs.graph import DAG
from job import JobState
from collections import Counter
import time


class LocalScheduler(object):
    def __init__(self):
        self._dag = DAG()
        self._inst_map = {}

    def _get_class_instance(self, cls):
        if cls not in self._inst_map:
            self._inst_map[cls] = cls()
        inst = self._inst_map[cls]
        return inst

    def add_job(self, cls):
        inst = self._get_class_instance(cls)
        dependencies = inst.requires() or []
        self._dag.add_node(inst)
        for dep_class in dependencies:
            dep = self._get_class_instance(dep_class)
            self._dag.add_edge(dep, inst)

    def check_valid(self):
        if not self._dag.is_valid():
            raise InvalidPipelineException("Pipeline contains a cycle.")

    def get_state(self):
        count = Counter(job.get_state() for job in self._dag.nodes_iter())
        return count

    def execute(self):
        sorted_nodes = self._dag.get_topological_sort()

        count = self.get_state()
        while not self._finished(count):
            for job in sorted_nodes:
                if job.is_complete():
                    sorted_nodes.remove(job)
                elif self._check_reqs_sat(job):
                    job.execute()

            time.sleep(1)
            count = self.get_state()
            print(count)

    def _finished(self, count):
        total_jobs = self._dag.number_of_nodes()
        return total_jobs == count[JobState.DONE] or count[JobState.FAILED] > 0

    def _check_reqs_sat(self, job):
        parents = [self._inst_map[x].is_complete() for x in job.requires() or []]
        return all(parents)

class InvalidPipelineException(Exception):
    pass

def _count_completed_and_failed_jobs(count):
    return count[JobState.DONE] + count[JobState.FAILED]