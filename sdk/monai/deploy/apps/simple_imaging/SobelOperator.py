import sys
sys.path.insert(0,'../../../../')

from skimage import data, io, filters
from monai.deploy.foundation import BaseOperator

class SobelOperator(BaseOperator.BaseOperator):
    def __init__(self):
        super().__init__()
        self.data_out = None
    

    def get_output(self, index):
        return self.data_out
    

    def execute(self):
        data_in = data.moon()
        self.data_out = filters.sobel(data_in)