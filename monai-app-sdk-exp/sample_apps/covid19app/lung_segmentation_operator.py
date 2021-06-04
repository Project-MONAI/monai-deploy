from monai.operators import ImageSegmentationOperator
from monai.foundation import ClaraImage
from cucim import CuImage
from cucim import Operation as CuCIMOperation


class LungSegmentationOperator(ImageSegmentationOperator):

    """
    This class performs Lung Segmentation based on a
    trained DL Model. The model it uses was traine using
    TensorFlow. This class is derived
    from ImageSegmentationOperator
    """

    def init(self):
        """
        This is a method that initializes the operator.
        This method executes only once of the life cycle of the operator
        """
        super().init(self)
        self.super().model = TensorFlowSavedModel(app_config.LUNG_SEGMENTATION_MODEL_PATH)
        self.super().inferer = SlidingWindowInferer()
    


    def pre_execute(self):
        """
        This method is called right before the operator is executed
        """
        self.super().pre_execute()

   
    def pre_process(self):
        """
        We have overriding this method from the base class
        This method is used right before inference is done

        Returns
        ----------------------
        out: MONAIImage
        """
        # here using cuCIM we perform some preprocessing
        input_image = CuImage(self.super().get_parent().get_output().tensor())
        rescale = CuCIMOperation('transforms.resample', x_spacing=1.0, y_spacing=1.0, z_spacing=1.0)
        output_image = rescale(input_image.read_region())
        return MONAIImage(output_image)


    def post_process(self):
        """
        We have overriding this method from the base class
        This method is used right after inference is done
        """
        self.super().post_process()
        pass


    def post_execute(self):
        """
        This method is called right before the operator is executed
        """
        self.super().post_execute()
