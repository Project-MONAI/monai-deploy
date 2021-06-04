import sys
sys.path.insert(0,'../../../../')
from monai.deploy.foundation.application import Application
from monai.deploy.apps.simple_imaging_app.sobel_operator import SobelOperator
from monai.deploy.apps.simple_imaging_app.median_operator import MedianOperator
from monai.deploy.apps.simple_imaging_app.gaussian_operator import GaussianOperator
from monai.deploy.executors.single_process_executor import SingleProcessExecutor

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
