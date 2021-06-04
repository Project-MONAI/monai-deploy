import sys
sys.path.insert(0,'../../../../')
from monai.deploy.foundation.Application import Application
from monai.deploy.apps.simple_imaging.SobelOperator import SobelOperator
from monai.deploy.apps.simple_imaging.MedianOperator import MedianOperator
from monai.deploy.apps.simple_imaging.GaussianOperator import GaussianOperator
from monai.deploy.executors.SingleProcessExecutor import SingleProcessExecutor

from skimage import data, io, filters

class MyApp(Application):
    def __init__(self):
        super().__init__()
        
    def compose(self):
        self.sobel_op = SobelOperator()
        self.median_op = MedianOperator()
        self.gaussian_op = GaussianOperator()
        self.link_operators(self.sobel_op, self.median_op)
        self.link_operators(self.median_op, self.gaussian_op)


app = MyApp()
executor = SingleProcessExecutor(app)
executor.execute()
