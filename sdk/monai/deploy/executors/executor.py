from abc import ABC, abstractmethod
from monai.deploy.foundation.application import Application

class Executor(ABC):

    def __init__(self, app):
        super().__init__()
        self._app = app
        self._app.compose()
        self._root_nodes = [n for n,d in self._app.get_graph().in_degree() if d==0]


    @abstractmethod
    def execute(self):
        pass
