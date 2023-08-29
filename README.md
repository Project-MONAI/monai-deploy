<p align="center">
  <img src="https://raw.githubusercontent.com/Project-MONAI/MONAI/dev/docs/images/MONAI-logo-color.png" width="50%" alt='project-monai'>
</p>

# MONAI Deploy Working Group

MONAI Deploy aims to become the de-facto standard for developing, packaging, testing, deploying and running medical AI applications in clinical production.

If you want to know more about its purpose and vision, please review the [**MONAI Deploy WG wiki**](https://github.com/Project-MONAI/MONAI/wiki/Deploy-Working-Group).

## Focus

MONAI Deploy builds on the foundation set by [MONAI](https://github.com/Project-MONAI/MONAI/).  

Where **MONAI** is focused on training and creating models, **MONAI Deploy** is focused on defining the journey from research innovation to clinical production environments in hospitals. Our guiding principles are:
- Implementation mindset. Create tangible assets: tools, applications and demos/prototypes.
- Radiology first, then other modalities like Pathology.
- Interoperability with clinical systems. Starting with DICOM, then FHIR.
- Central repository to facilitate collaboration among institutions.

## Status

MONAI Deploy was released at **MICCAI 2021** and was part of the [**MONAI 2021 Bootcamp**](https://www.gpuhackathons.org/event/monai-miccai-bootcamp-2021). Since then we have released several versions of some of the sub-systems, while others are being actively developed. Please check out the next section.

## Key assets
- [**MONAI Application Package (MAP)**](https://github.com/Project-MONAI/monai-deploy/blob/main/guidelines/monai-application-package.md) - defines how applications can be packaged.
    and distributed amongst MONAI Working Group member organizations.
- [**MONAI Deploy App SDK**](https://github.com/Project-MONAI/monai-deploy-app-sdk) - set of development tools to create MAPs out of MONAI / Pytorch models.
- [**MONAI Deploy Informatics Gateway**](https://github.com/Project-MONAI/monai-deploy-informatics-gateway) - I/0 for DICOM and FHIR.
- [**MONAI Deploy Workflow Manager**](https://github.com/Project-MONAI/monai-deploy-workload-manager) - Orchestrates what has to be executed based on the [**clinical workflow specification**](https://github.com/Project-MONAI/monai-deploy-workflow-manager/blob/main/docs/setup/mwm-workflow-spec.md) and incoming requests.
- [**MONAI Deploy Express**](https://github.com/Project-MONAI/monai-deploy/tree/main/deploy/monai-deploy-express) - End-to-end pipeline for testing and validation of MONAI Applications (MAPs).


## Community

To participate, please join the MONAI Deploy WG weekly meetings on the [calendar](https://calendar.google.com/calendar/u/0/embed?src=c_954820qfk2pdbge9ofnj5pnt0g@group.calendar.google.com&ctz=America/New_York). All the recordings and meeting notes since day zero can be found at [MONAI Deploy WG master doc](https://docs.google.com/document/d/1fzG3z7TxB9SzWdfqsApAMFrM91nHfYiISnSz4QHJHrM/)

Join our [Slack channel](https://forms.gle/QTxJq3hFictp31UM9) or join the conversation on Twitter [@ProjectMONAI](https://twitter.com/ProjectMONAI).

Ask and answer questions over on [MONAI Deploy's GitHub Discussions tab](https://github.com/Project-MONAI/monai-deploy/discussions) or [MONAI's GitHub Discussions tab](https://github.com/Project-MONAI/MONAI/discussions).

## Links

- Website: <https://monai.io>
- Guidelines: <https://docs.monai.io/projects/monai-deploy/guidelines>
- Roadmap tracker: <https://github.com/Project-MONAI/monai-deploy/projects>
- Issue tracker: <https://github.com/Project-MONAI/monai-deploy/issues>
