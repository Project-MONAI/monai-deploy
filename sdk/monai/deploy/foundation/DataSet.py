from abc import ABC, abstractmethod
import uuid



class DataSet(ABC):
    pass

    @abstractmethod
    def get_data(self):
        pass

    