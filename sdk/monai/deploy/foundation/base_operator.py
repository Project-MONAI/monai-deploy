from abc import ABC, abstractmethod
import uuid
from monai.deploy.foundation.state_service import StateService


class BaseOperator(ABC):

    def __init__(self):
        super().__init__()
        self._storage = StateService.get_instance()
        self._num_input_ports = 1
        self._num_output_ports = 1
        self._child_index = 0
        self._uid = uuid.uuid4()
        

    def get_uid(self):
        return self._uid
   

    def get_input(self, index):
        return self._storage.retrieve((self.get_uid(), 'input', index))
    

    @abstractmethod
    def get_output(self, index):
        pass
    

    def get_num_input_ports(self):
        return self._num_input_ports
    

    def get_num_output_ports(self):
        return self._num_output_ports
        
    
    def pre_execute(self):
        pass

    @abstractmethod
    def execute(self):
        pass


    def post_execute(self):
        pass

