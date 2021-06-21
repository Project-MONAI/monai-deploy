import sys
sys.path.insert(0,'../../../../')

from skimage import data, io, filters
from monai.deploy.foundation.base_operator import BaseOperator

class SobelOperator(BaseOperator):
    def __init__(self):
        super().__init__()
        self.data_out = None
    

    def get_output(self, output_port_number):
        return self.data_out
    

    def execute(self):
        super().execute()
        data_in = io.imread("./brain_mr_input.jpg")
        self.data_out = filters.sobel(data_in)