<p align="center">
  <img src="https://raw.githubusercontent.com/Project-MONAI/MONAI/dev/docs/images/MONAI-logo-color.png" width="50%" alt='project-monai'>
</p>

# MONAI Deploy Working Group test

MONAI Deploy aims to become the de-facto standard for developing, testing, deploying and running medical AI applications in clinical production.

If you want to know more about its purpose and vision, please review the <https://github.com/Project-MONAI/MONAI/wiki/Deploy-Working-Group>.

## Focus

MONAI Deploy builds on the foundation set by [MONAI](https://github.com/Project-MONAI/MONAI/).  

Where **MONAI** is focused on training and creating models, **MONAI Deploy** is focused on defining the journey from research innovation to clinical production environments in hospitals. Our guiding principles are:
- Implementation mindset. Create tangible assets: tools, applications and demos/prototypes.
- Radiology first, then other modalities like Pathology.
- Interoperability with clinical systems. Starting with DICOM, then EHR.
- Central repository to facilitate collaboration among institutions.

## Sub-systems
First version, **v0.1.0** includes:
- **MONAI Application Package (MAP)** - defines how applications can be packaged.
    and distributed amongst MONAI Working Group member organizations.
- [**MONAI Deploy App SDK**](https://github.com/Project-MONAI/monai-deploy-app-sdk) - set of development tools to create MAPs out of MONAI / Pytorch models.

Future versions will include:
- **MONAI Deploy Informatics Gateway** - I/0 for DICOM and FHIR.
- **MONAI Deploy Workload Manager** - Orchestrates what has to be executed based on incoming patient requests.
- **MONAI Deploy Server** - Server environment which can run MONAI Applications (MAPs).

## Status

MONAI Deploy will be released at **MICCAI 2021** and will be part of the **MONAI Bootcamp**. Sign up to know more! 

## Community

To participate in the MONAI Deploy WG, please review the [MONAI Deploy WG Wiki page](https://github.com/Project-MONAI/MONAI/wiki/Deploy-Working-Group).
All the recordings and meeting notes since day zero can be found at [MONAI Deploy WG master doc](https://docs.google.com/document/d/1fzG3z7TxB9SzWdfqsApAMFrM91nHfYiISnSz4QHJHrM/)

Join our [Slack channel](https://forms.gle/QTxJq3hFictp31UM9) or join the conversation on Twitter [@ProjectMONAI](https://twitter.com/ProjectMONAI).

Ask and answer questions over on [MONAI Deploy's GitHub Discussions tab](https://github.com/Project-MONAI/monai-deploy/discussions) or [MONAI's GitHub Discussions tab](https://github.com/Project-MONAI/MONAI/discussions).

## Links

- Website: <https://monai.io>
- Guidelines: <https://docs.monai.io/projects/monai-deploy/guidelines>
- Roadmap tracker: <https://github.com/Project-MONAI/monai-deploy/projects>
- Issue tracker: <https://github.com/Project-MONAI/monai-deploy/issues>
