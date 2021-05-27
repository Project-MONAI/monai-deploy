from monai.operators import MMAROperator
from monai.foundation.similarity_metric import JaccardIndex
from covid19app import app_config


class GGOLesionSegmentationOperator(SegmentationOperator):

    """
    This is a custom class derived from the built-in SegmentationOperator
    """

    def init(self):
        """
        This is a method that initializes the operator.
        This method executes only once of the life cycle of the operator
        """
        self.super().init()



    def pre_execute(self):
        """
        This method is called right before the operator is executed
        """
        # here we set path to a gold stanard for input & output
        self.super().set_verification_data(app_config.GGO_SEGMENTATION_GOLD_INPUT_PATH
        app_config.GGO_SEGMENTATION_GOLD_OUTPUT_PATH)

        # here we specify a similarity measure
        self.super().set_similarity_metric(JaccardIndex(0.9, 1.0))



    # The second decorator is rquesting that the first input 
    # dataset (which is a volumetric image) be rendered
    # in the development console using volume rendering mode
    # with a specified transfer function
    @render(input_data_index=0, default_view_mode = 'orig_slice')
    def execute():
        """
        This is the method clara framework calls to execute the operator.
        Bacause this is a built in classification operator
        that makes use of an MMAR model, the built-in behavior
        is sufficient. However the code below is shown just in-case
        the user wants to customize


        Returns
        ----------------
        out: MaskedImage
        """

        # retrieve the output from the previous operator
        tensor = self.super().get_parent_operator().get_output()

        # first call pre-process
        self.super().pre_process(tensor)

        # now do the actual predicition
        pred = self.super().perform_inference(tensor)

        # do some post processing
        self.super().post_process()

        return pred



    def post_execute(self):
        """
        This method is called right before the operator is executed
        """
        self.super().pre_execute()

        pass