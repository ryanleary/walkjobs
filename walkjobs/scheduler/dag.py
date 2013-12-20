from copy import copy, deepcopy


class DAG(object):

    def __init__(self):
        self.graph = {}

    def add_node(self, node_name):
        if node_name in self.graph:
            raise KeyError("Node %s already exists." % node_name)
        self.graph[node_name] = set()

    def rename_node(self, old_name, new_name):
        for node, edges in self.graph.iteritems():
            if node == old_name:
                self.graph[new_name] = copy(edges)
                del self.graph[old_name]
            else:
                if old_name in edges:
                    edges.remove(old_name)
                    edges.add(new_name)

    def delete_node(self, node_name):
        self.__check_node_exists(node_name)

        self.graph.pop(node_name)
        for node, edges in self.graph.iteritems():
            if node_name in edges:
                edges.remove(node_name)

    def add_edge(self, source, sink):
        self.__check_node_exists(source)
        self.__check_node_exists(sink)

        self.graph[source].add(sink)

    def delete_edge(self, source, sink):
        self.__check_node_exists(source)
        if sink not in self.graph.get(source, []):
            raise KeyError('Edge does not exist in graph.')
        self.graph[source].remove(sink)

    def get_children(self, node_name):
        self.__check_node_exists(node_name)
        return list(self.graph[node_name])

    def get_sources(self):
        all_nodes, sink_nodes = set(self.graph.keys()), set()
        for child_nodes in self.graph.itervalues():
            sink_nodes.update(child_nodes)
        return list(all_nodes - sink_nodes)

    def is_valid(self):
        if len(self.get_sources()) == 0:
            return False
        try:
            self.__topological_sort()
        except ValueError:
            return False
        return True

    def get_dependencies(self, target_node, graph=None):
        if graph is None:
            graph = self.graph

        result = set()
        for node, outgoing_nodes in graph.iteritems():
            if target_node in outgoing_nodes:
                result.add(node)
        return list(result)

    def __topological_sort(self):
        graph = deepcopy(self.graph)
        l = []
        s = deepcopy(self.get_sources())
        while len(s) != 0:
            n = s.pop(0)
            l.append(n)
            iter_nodes = deepcopy(graph[n])
            for m in iter_nodes:
                graph[n].remove(m)
                if len(self.get_dependencies(m, graph)) == 0:
                    s.append(m)

        if len(l) != len(graph.keys()):
            raise ValueError('graph is not acyclic')
        return l

    def __check_node_exists(self, node_name):
        if node_name not in self.graph:
            raise KeyError("Node %s does not exist." % node_name)