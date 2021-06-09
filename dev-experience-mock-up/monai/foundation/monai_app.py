from monai.operators import DataExportOperator
from monai.results_service import ResultsService
class MONAIApp:
    """
    The base class of all apps which provides helper methods to export data, load and access configurations, etc...
    """
    def __init__(self) -> None:
        self._settings = self._load_config()
        self._data_export_op = DataExportOperator()


    def _load_config(self) -> None:
        """
        loads application configurations
        """
        pass

    # def export_dicom(self, data) -> None:
    #     """
    #     registers `data` with Results Service 2.0 for export to configured DICOM destinations via SCU
    #     """
    #     for dest in self.settings.export.dicom:
    #         self._export(dest, data)

    # def export_dicom_web(self, data) -> None:
    #     """
    #     registers `data` with Results Service 2.0 for export to configured DICOM Web destinations
    #     """
    #     for dest in self.settings.export.dicomweb:
    #         self._export(dest, data)

    # def export_fhir(self, data) -> None:
    #     """
    #     registers `data` with Results Service 2.0 for export to configured FHIR servers
    #     """
    #     for dest in self.settings.export.fhir:
    #         self._export(dest, data)

    # def _export(self, dest, data) -> None:
    #     """
    #     calls the Results Service 2.0 API to register data for export
    #     """
    #     api = ResultsService()
    #     api.register(dest, data)