# import the necessary packages
import os

# define the base path and then use it to derive
# all the other paths
BASE_PATH = "."

# model paths
COVID19_CLASSIFICATION_MODEL_PATH = os.path.sep.join([BASE_PATH, "covid_classification"])
LUNG_SEGMENTATION_MODEL_PATH = os.path.sep.join([BASE_PATH, "lung_segmentation"])

# gold truth data paths
COVID19_CLASSIFICATION_GOLD_INPUT_PATH = os.path.sep.join([BASE_PATH, "covid_classification_gold_input"])
COVID19_CLASSIFICATION_GOLD_OUTPUT_PATH = os.path.sep.join([BASE_PATH, "covid_classification_gold_output"])
GGO_SEGMENTATION_GOLD_INPUT_PATH = os.path.sep.join([BASE_PATH, "ggo_segmentation_gold_input"])
GGO_SEGMENTATION_GOLD_OUTPUT_PATH = os.path.sep.join([BASE_PATH, "ggo_segmentation_gold_output"])


# PACS Info
PACS_AE_1 = "Cardiology_PACS"
PACS_AE_1_PORT = "5596"