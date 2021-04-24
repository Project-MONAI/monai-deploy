from monai.deploy import ProcessTask, T1MRI, SegMask
import numpy as np
import torch

class TumourVolumeTask(ProcessTask):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_uri = "models://someplace"
        self.autoprocess = True  # flag to permit autoprocessing
        input = T1MRI: Dicom
        output = SegMask: Dicom

    @property
    def valid(self):
        if 't1' in self.study.keys() and 'brain' in self.study.keys():
            return True
        elif self.study.series[0].SeriesDescripton=='T1W':
            return False
    
    def get_t1_vol(study: Study):
        return torch.from_numpy(self.study['t1'].pixel_array)
        

    def process(self):

        model.load_state_dict(torch.load(model_location))
        model.eval()
        with torch.no_grad():
            val_input = get_t1_vol(self.study).to(device)
            val_output = model(val_input)

        voxel_volume = self.study.pixel_spacing[0] * self.study.pixel_spacing[0] * self.study.slice_thickness
        tumor_volume = voxel_volume * np.count_nonzero(val_output)

        table = {"Measurement": "Tumor Volume", "Value": f"{tumor_volume} mm^3"}

        self.archive_pacs((val_output, table), kind='SecondaryCapture+table', review=False)
    