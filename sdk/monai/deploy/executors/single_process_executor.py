from abc import ABC, abstractmethod
from monai.deploy.foundation.data_store import DataStore
from monai.deploy.executors.executor import Executor
import networkx as nx
from queue import Queue

class SingleProcessExecutor(Executor):

    def __init__(self, app):
        super().__init__(app)
        self._storage = DataStore.get_instance()


    def execute(self):
        g = self._app.get_graph()
        #edges = nx.bfs_edges(g)
        #nodes = [self._root_nodes[0]] + [v for u, v in edges]
        nodes_old = [list(nx.bfs_tree(g, n)) for n in self._root_nodes]
        nodes = [item for sublist in nodes_old for item in sublist]

        for node in nodes:
            node.pre_execute()
            node.execute()
            node.post_execute()
            edges = g.out_edges(node)
            for e in edges:
                    edge_data = g.get_edge_data(e[0], e[1])
                    output = node.get_output(edge_data['upstream_op_port'])
                    key1 = (e[0].get_uid(), 'output', edge_data['upstream_op_port'])
                    self._storage.store(key1, output)
                    key2 = (e[1].get_uid(), 'input', edge_data['downstream_op_port'])
                    self._storage.store(key2, output)



    def execute2(self):
        g = self._app.get_graph()
        for node in self._root_nodes:

            q = Queue()
            q.put(node)

            while(q.empty() == False):
                n = q.get()
                edges = g.out_edges(n)
                n.execute()

                for e in edges:

                    #figure out how to deal with duplicate nodes
                    q.put(e[1])
                    edge_data = g.get_edge_data(e[0], e[1])
                    output = node.get_output(edge_data['upstream_op_port'])
                    key1 = (e[0].get_uid(), 'output', edge_data['upstream_op_port'])
                    self._storage.store(key1, output)
                    key2 = (e[1].get_uid(), 'input', edge_data['downstream_op_port'])
                    self._storage.store(key2, output)




#https://cole-maclean-networkx.readthedocs.io/en/latest/reference/algorithms/generated/networkx.algorithms.traversal.breadth_first_search.bfs_edges.html



        
