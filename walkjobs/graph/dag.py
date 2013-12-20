import networkx as nx


class DAG(nx.DiGraph):

    def __init__(self):
        nx.DiGraph.__init__(self)

    def get_ancestors(self, node):
        return nx.ancestors(self, node)

    def get_descendants(self, target_node, graph=None):
        if not graph:
            graph = self
        return nx.descendants(graph, target_node)

    def get_sources(self):
        return set([n for n in self.nodes_iter() if self.in_degree(n) == 0])

    def is_valid(self):
        return nx.is_directed_acyclic_graph(self)
