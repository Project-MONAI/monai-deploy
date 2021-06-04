from monai.operators import ImageSegmentationOperator
from monai.foundation import ClaraImage
from monai.clinical import LungWorkflow
from cucim import CuImage
from cucim import Operation as CuCIMOperation


class LungROIDetectionOperator(GPGPUOperator):

    """
    This class performs detetcion of Lung ROI
    It makes use of computer vision methods
    as provided by the monai.clinical package
    """

    def init(self):
        """
        This is a method that initializes the operator.
        This method executes only once of the life cycle of the operator
        """
        super().init(self)



    def pre_execute(self):
        """
        This method is called right before the operator is executed
        """
        self.super().pre_execute()

   
    def execute(self):
        self.super().execute()
        # make use monai.clinical package to detect the lung boundary


    def post_execute(self):
        """
        This method is called right before the operator is executed
        """
        self.super().post_execute()


