import sys
sys.path.insert(0,'../../../../')

from monai.deploy.foundation.BaseOperator import BaseOperator

from skimage import data
from skimage.morphology import disk
from skimage.filters import gaussian
from skimage.io import imsave

class GaussianOperator(BaseOperator):
    def __init__(self):
        super().__init__()
        self.data_out = None
    

    def get_output(self, index):
        return self.data_out
    

    def execute(self):
        data_in = self.get_input(0)
        self.data_out = gaussian(data_in, sigma=0.4)
        imsave("final_output.png", self.data_out)
