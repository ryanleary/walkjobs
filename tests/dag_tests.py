from walkjobs.scheduler.dag import DAG
import unittest


class DAGTestCases(unittest.TestCase):
    def get_graph_a(self):
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

    def get_graph_b(self):
        dag = DAG()

        # add nodes
        dag.add_node("A")
        dag.add_node("B")
        dag.add_node("C")

        # add edges
        dag.add_edge("B", "A")
        dag.add_edge("C", "A")

        return dag

    def get_invalid_graph(self):
        dag = self.get_graph_a()

        # add edge to create cycle
        dag.add_edge("F", "D")

        return dag

    def test_valid_dag_is_valid(self):
        dag = self.get_graph_a()
        assert (dag.is_valid())

    def test_invalid_dag_is_valid(self):
        dag = self.get_invalid_graph()
        assert (not dag.is_valid())

    def test_valid_dag_get_sources_a(self):
        dag = self.get_graph_a()
        assert (dag.get_sources() == ['B'])

    def test_valid_dag_get_sources_b(self):
        dag = self.get_graph_b()
        assert (check_equal(dag.get_sources(), ['B', 'C']))

    def test_valid_get_dependencies(self):
        dag = self.get_graph_a()

        assert (dag.get_dependencies('A') == ['B'])
        assert (dag.get_dependencies('B') == [])
        assert (check_equal(dag.get_dependencies('C'), ['A', 'D']))
        assert (dag.get_dependencies('D') == ['B'])
        assert (dag.get_dependencies('E') == ['C'])
        assert (dag.get_dependencies('F') == ['C'])

    def test_add_invalid_edge_source(self):
        dag = self.get_graph_a()
        with self.assertRaises(KeyError):
            dag.add_edge('X', 'C')

    def test_add_invalid_edge_sink(self):
        dag = self.get_graph_a()
        with self.assertRaises(KeyError):
            dag.add_edge('C', 'X')


def check_equal(list_a, list_b):
    return len(list_a) == len(list_b) and sorted(list_a) == sorted(list_b)


if __name__ == '__main__':
    unittest.main()
