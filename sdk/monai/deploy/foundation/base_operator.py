from abc import ABC, abstractmethod
import uuid
import os
from monai.deploy.foundation.data_store import DataStore
from colorama import Fore, Back, Style


class BaseOperator(ABC):

    def __init__(self):
        super().__init__()
        self._storage = DataStore.get_instance()
        self._num_input_ports = 1
        self._num_output_ports = 1
        self._uid = uuid.uuid4()
        

    def get_uid(self):
        return self._uid
   


    def set_input(self, name, val):
        pass
    

    def get_output(self, name, val):
        pass

   

    def get_input(self, input_port_number):
        return self._storage.retrieve((self.get_uid(), 'input', input_port_number))
    


    @abstractmethod
    def get_output(self, output_port_number):
        pass
    

    def get_num_input_ports(self):
        return self._num_input_ports
    

    def get_num_output_ports(self):
        return self._num_output_ports
        
    
    def pre_execute(self):
        print(Fore.BLUE + 'Going to initiate execution of operator %s' %self.__class__.__name__)
        '%s is smaller than %s' % ('one', 'two')
        pass

    @abstractmethod
    def execute(self):
        print(Fore.YELLOW + 'Process ID %s' % os.getpid())
        print(Fore.GREEN + 'Executing operator %s' %self.__class__.__name__)
        # print('parent process: ', os.getppid())
        pass


    def post_execute(self):
        print(Fore.BLUE + 'About to complete executtion of operator %s' % self.__class__.__name__)
        pass

