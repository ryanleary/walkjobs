import unittest

from walkjobs.graph import DAG


class DAGTestCases(unittest.TestCase):
    def setUp(self):
        self.graph_a = generate_graph_a()
        self.graph_b = generate_graph_b()
        self.invalid_graph = generate_invalid_graph()

    def test_valid_dag_is_valid(self):
        assert (self.graph_a.is_valid())

    def test_invalid_dag_is_valid(self):
        assert (not self.invalid_graph.is_valid())

    def test_valid_dag_get_sources_a(self):
        assert (self.graph_a.get_sources() == set(['B']))

    def test_valid_dag_get_sources_b(self):
        assert (self.graph_b.get_sources() == set(['B', 'C']))

    def test_valid_dag_get_ancestors(self):
        assert (self.graph_a.get_ancestors('A') == set(['B']))
        assert (self.graph_a.get_ancestors('B') == set([]))
        assert (self.graph_a.get_ancestors('C') == set(['A', 'B', 'D']))
        assert (self.graph_a.get_ancestors('D') == set(['B']))
        assert (self.graph_a.get_ancestors('E') == set(['C', 'A', 'B', 'D']))
        assert (self.graph_a.get_ancestors('F') == set(['C', 'A', 'B', 'D']))

    def test_valid_dag_get_descendants(self):
        assert (self.graph_a.get_descendants('A') == set(['C', 'F', 'E']))


def generate_graph_a():
    #  A --> C --> E
    #  ^     ^ \
    #  |     |   \
    #  B --> D     F
    # (c to f)
    dag = DAG()

    # add nodes
    dag.add_node("A")
    dag.add_node("B")
    dag.add_node("C")
    dag.add_node("D")
    dag.add_node("E")
    dag.add_node("F")

    # add edges
    dag.add_edge("A", "C")
    dag.add_edge("B", "A")
    dag.add_edge("B", "D")
    dag.add_edge("D", "C")
    dag.add_edge("C", "E")
    dag.add_edge("C", "F")

    return dag


def generate_graph_b():
    dag = DAG()

    # add nodes
    dag.add_node("A")
    dag.add_node("B")
    dag.add_node("C")

    # add edges
    dag.add_edge("B", "A")
    dag.add_edge("C", "A")

    return dag


def generate_invalid_graph():
    dag = generate_graph_a()

    # add edge to create cycle
    dag.add_edge("F", "D")

    return dag

if __name__ == '__main__':
    unittest.main()
