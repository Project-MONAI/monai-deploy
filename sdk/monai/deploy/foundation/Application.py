from abc import ABC, abstractmethod
import networkx as nx


class Application(ABC):

    def __init__(self):
        super().__init__()
        self._graph = nx.DiGraph()


    def get_graph(self):
        return self._graph


    def link_operators(self, upstream_op, downstream_op, upstream_op_port=0, downstream_op_port=0):
        self._graph.add_edge(upstream_op, downstream_op, upstream_op_port=upstream_op_port, downstream_op_port=downstream_op_port)
        pass

    @abstractmethod
    def compose(self):
        pass

