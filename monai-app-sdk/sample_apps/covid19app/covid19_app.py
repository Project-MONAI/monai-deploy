from monai.foundation import MONAIApp
from monai.operators import DICOMSeriesLoaderOperator
from monai.operators import DICOMSRComposeOperator
from monai.foundation import RouterRegistry
from covid19app.lung_segmentation_operator import LungSegmentationOperator
from covid19app.ggo_lesion_seg_operator import GGOLesionSegmentationOperator
from covid19app.vol_ratio_comp_operator import VolumeRatioComputeOperator
from covid19app.covid_classification_operator import COVID19ClassificationOperator
from covid19app.lung_roi_detetcion_operator import LungROIDetectionOperator


class COVID19App(MONAIApp):

    """
    MONAI App Developer SDK provides a framework for building healthcare
    apps. Each Application is inherited from the base HealthcareApp
    class. A healthcare app has the following lifecycle methods:

    init: This method gets called to initialize the application. This is called
    only once. 

    compose: This method gets called after init. This is where all the operators
    in the app get composed to form a DAG like structure.

    pre_execute: Framework calls this method before an app execution starts. This gives
    an opportunity to the app to make sure that all preconditions are valid before 
    the app can be executed

    execute: Framework calls this method to execute the app. Most applications do
    not need to override it. 

    post_execute: Framework calls this method after execution of the application is over.
    Applications can override it to clean up resources if needed.

    COVID19App is a multi-staged application. Each stage is represented by an 
    Operator instance. These Operators are composed in a DAG structure.

    """

    def init(self):
        """
        This is the method that initializes the application with the required operators 
        inside it. This method executes only once of the life cycle of an app.
        This is the place where we instantiate all necessary operators
        """
        # First we need to instantiate all the operators
        # needed for this op
        self.dicom_series_loader_op = DICOMSeriesLoaderOperator()
        self.lung_roi_detetcor_op = LungROIDetectionOperator()
        self.lung_seg_op = LungSegmentationOperator()
        self.ggo_lesion_seg_op = GGOLesionSegmentationOperator()
        self.covid_classification_op = COVID19ClassificationOperator()
        self.vol_ratio_comp_op = VolumeRatioComputeOperator()
        self.dicom_sr_compose_op = DICOMSRComposeOperator()
        self.dicom_push_op = DICOMPushOperator()

    def compose(self):
        """
        This is the method where the app composes a pipeline
        out of all operators. Each operator has a next method
        using which a downstream (child) operator can be added to an
        upstream (parent) operator. A single operator can have multiple
        upstream operators

        """
        # Here we chain up all the operators in the form of a DAG

        # The first operator is the DICOM Series Loader Operator
        # It loads a single DICOM Series from disk and provides
        # an in-memory representation of the Imaging Data, an instance of ClaraImage

        # The second operator is the Lung ROI Operator
        # It makes use of computer vision methods offered by the monai.clinical package
        # to detect a tight 3D bounding box around the Lung
        # Input: dicom series loader
        # Output: a MONAIImage
        self.dicom_series_loader_op.next(self.lung_roi_detetcor_op)

        # The this operator is the Lung Segmentation Operator
        # It makes use of a DL Model to segment Lung voxels
        # The segmented lung voxels are represented using an in-memory mask
        # Input: dicom series loader
        # Output: a MaskedImage (derived from MONAIImage)
        self.lung_roi_detetcor_op.next(self.lung_seg_op)

        # The fourth operator is a ground glass opacity segmentation operator.
        # It also makes use of a DL Model
        # Input to the ground-glass-opacity lesion segmentation operator is the DICOM Series Loader
        # Output is a MaskedImage (derived from MONAIImage)
        self.dicom_series_loader_op.next(self.ggo_lesion_seg_op)

        # The fifth operator is a covid lesion classification operator.
        # It also makes use of a DL Model
        # Inputs are original DICOM Series Loader ground glass opacity segmentation operator
        # Output is a MaskedImage
        self.dicom_series_loader_op.next(self.covid_classification_op)
        self.ggo_lesion_seg_op.next(self.covid_classification_op)

        # The sixth operator is a volume ratio compute.
        # Inputs are segmented lung & ggo segmented lesions
        # Output is is of type NumericInfo
        self.lung_seg_op.next(self.vol_ratio_comp_op)
        self.ggo_lesion_seg_op.next(self.vol_ratio_comp_op)

        # the seventh operator is a DICOM SR Composer
        # it ingests the output from vol_ratio_op
        # and produces a SRReport
        self.vol_ratio_comp_op.next(self.dicom_sr_compose_op)

        # the last operator is something that takes the SR object and
        # makes a request to push to a DICOM SCP
        self.dicom_sr_compose_op.next(self.dicom_push_op)

    def pre_execute(self):
        self.super().pre_execute()

    def post_execute(self):
        self.super().post_execute()