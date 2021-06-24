from abc import ABC, abstractmethod
import networkx as nx


class Application(ABC):

    """ This is the base application class
    All applications should be extended from this Class
    The application class provides support for chaining
    
    """

    def __init__(self):
        """ This is the base application class
        All applications should be extended from this Class

   
        Args:
        input_shape: Single tuple, TensorShape, or list/dict of shapes, where
            shapes are tuples, integers, or TensorShapes.
        
        Raises:
        ValueError:
            1. In case of invalid user-provided data (not of type tuple,
            list, TensorShape, or dict).
            2. If the model requires call arguments that are agnostic
            to the input shapes (positional or kwarg in call signature).
            3. If not all layers were properly built.
            4. If float type inputs are not supported within the layers.
        In each of these cases, the user should build their model by calling it
        on real tensor data.
        """


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

