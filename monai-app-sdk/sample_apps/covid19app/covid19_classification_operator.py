from monai.operators import MultiClassClassificationOperator
from monai.operators import Prediction
from covid19app import app_config


class COVID19ClassificationOperator(MultiClassClassificationOperator):


    render_config = {
        "input_data_ports" = "0,1",
        "input_viewing_modes" = "original, dvr",
        "output_data_ports" = "0",
        "output_viewing_modes" = "dvr"
    }
    def init(self):
        """
        This is a method that initializes the operator.
        This method executes only once of the life cycle of the operator
        """
        # here we first instantiate the model
        self.super().model = MMARModel(app_config.COVID19_CLASSIFICATION_MODEL_PATH)

        # MMAR model types are different, as they already prescribe what
        # type of inference to use. So, we query the MMAR and instantiate
        # the right type of inferer
        if self.model.configured_inferer = InfererType.SIMPLE:
            self.super().inferer = SimpleInferer()
        elif:
            self.super().inferer = SlidingWindowInferer()


    def pre_execute(self):
        """
        This lifecycle method is called right before an operator is invoked
        """
        # here we set path to a gold stanard for input & output
        self.super().set_verification_data(app_config.COVID19_CLASSIFICATION_MODEL_GOLD_INPUT_PATH, 
        app_config.COVID19_CLASSIFICATION_MODEL_GOLD_OUTPUT_PATH)



    def pre_process(self):
        """
        We have overriding this method from the base class
        This method is used before inference is done

        Returns
        ----------------------
        out: MONAIImage
        """
        # here using cuCIM we perform some preprocessing
        input_image_1 = CuImage(self.super().get_parent().get_output(0).tensor())
        input_image_2= CuImage(self.super().get_parent().get_output(0).tensor())
        intersect = CuCIMOperation('intersection')
        output_image = intersect(input_image_1.read_region(), input_image_2.read_region())
        return MONAIImage(output_image)


    # The second decorator is rquesting that as specified in the render
    # config, the system should render input & output datasets using the
    # appropriate visualization modes
    @render(render_config = COVID19ClassificationOperator.render_config)


    # the third decorator is requesting that this operator
    # be profiled, the input dataname should be retrieved from environment 
    # and all pofile information
    
    @profile(level=["operator", "kernel"], track=["system_memory", "gpu_memory"], color="purple")
    def execute():
        """
        This is the method monai app development sdk calls to execute the operator.
        Bacause this is a built in classification operator
        that makes use of an MMAR model, the built-in behavior
        is sufficient. However the code below is shown just in-case
        the user wants to customize the execute code


        Returns
        ----------------
        pred: Predicition
        """
        return self.super().execute()


    def post_process(self):
        return self.super().post_process()


    def post_execute(self):
        pass
