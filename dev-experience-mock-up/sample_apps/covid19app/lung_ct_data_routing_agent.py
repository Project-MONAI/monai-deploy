from typing import Dict
from monai.discovery import DataRouter
from monai.discovery import DICOMMetaDataRule


class LungCTDataRoutingAgent(DataRoutingAgent):

    """
    Each app needs have an Data Routing Agent attached to it
    The framework makes use of this instance to discover whether
    subset of the incmoing dataset should be provided as input
    to this app. Each data router instance evaluates a set of rules
    and figures out whether a data asset is relevant for one or more apps
    """

    def init(self):
        """
        This is a method of the Data Routing Agent class which gets invoked by the Framework 
        right after the app itself is initialized. In this case, we are going to give these 
        rulesets a name so that other apps can use it if desired
        """
        super("lung_ct_data_routing_agent")

        

    def execute(self, dataset):
        """
        This is a method the framework invokes whenever a dataset arrives at the storage layer of the Informatics 
        Gateway. Data Routing Agent instance in turn makes use of the dataset and evaluates some rules to figure out
        which data components of a dataset are relevant for this app


        Parameters
        ----------
        dataset : Dataset
        dataset is an instance of DICOMStudy or FHIRResource. It is one of the highest level
        of dataset types managed by the Informatics Gateway


        Returns
        -----------
        A list of jobs with all the data components that satisfy for each job

        """

        target_data_assets = List()

        # There are several types of dataset this framework supports. Examples
        # are FHIR, DICOMStudy, NIFTI etc. In this case we are only interested
        # in DICOM datasets
        if (isinstance (dataset, DICOMStudy)):
            # Now we know our dataset is of type study
            study = dataset

            # first rule is based on DICOM metadata. Let's check whether
            # the study modality is CT
            rule1 = DICOMMetaDataRule.evaluate(study, DICOMAttributes.modality, "EQUALS", "CT")

            # second rule is also based on DICOM metadata. Let's check whether
            # the body part is Lung.
            rule2 = DICOMMetaDataRule.evaluate(study, DICOMAttributes.body_part_examined, "EQUALS", "Lung")

            # So far we checked just DICOM headers. But we know that some of the attributes
            # may not be available in the header. Body Part is one such attribute. So we are
            # not going to just rely on DICOM Header. Next we are going to use an AI Model to
            # detect the modality of a series

            # third rule is whether body part is Lung based on image content
            rule3 = False
            for series in study.series_collection:
                if series.contains_volumetric_image():
                    pixel_data = sop.get_volumetric_image()
                    # process the pixel data
                    # # check for Modality based on an AI Model
                    # # if so, set rule 3 to be True
                    body_part_checker = BodyPartClassifierOperator()
                    body_part_checker.set_input_data(pixel_data.tensor())
                    pred = body_part_checker.execute()

                    if pred.body_part == BodyParts.Lung:
                        rule3 = True
                    
            
            if rule1 and (rule2 or rule3):
                # add the series is a target asset for this application
                target_datasets.add(series)

        return target_data_assets
    