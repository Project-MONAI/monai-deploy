### Introduction
There is a large chasm between training an AI model and deploying it to a production environment. In the healthcare domain, productization of an AI model involves more than just performing inference with a model. Issues such as ingestion of medical imaging datasets, performing application specific pre and post processing operations, as well as packaging output from the application so that it can be effectively pushed to the right informatics data sink - are all important aspects of app development. The MONAI Application SDK provides a framework to design, integrate and develop medical AI applications. 

---


### [REQ] Representing application specific tasks
The SDK shall enable representing a computational task in a healthcare application using an operator

#### Background
Most healthcare application workflows involves multiple tasks. Each task is a basic unit of work. Having a programmatic way of representing such task is important as this promotes seperation of concern, reusability and debuggability. Example of tasks are: loading a DICOM Series into an in-memory volumetric representation, ability to rescale a volumetric etc.

#### Verification Strategy
Verify that common set of workflow tasks can be represented by built-in Operators

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] Representing Workflow With DAG
The SDK shall enable designing application workflows by allowing upstream and downstream dependencies among multiple operators in an Applications

#### Background
Most healthcare application workflows involves multiple stages. Application developers need a way to organize functional units of AI based inference apps. A DAG (Directed Acyclic Graph) is the core concept of MONAI App SDK, collecting Operators together, organized with dependencies and relationships to say how they should run.

#### Verification Strategy
Build an application with the SDK which has multiple operators. Verify that the SDK offers a mechanism to represent the underlying worklfow using a DAG and enables traversal of the DAG

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] Representing Workflow with DCG
The SDK shall enable designing application workflows which can be represented by a Directed Cyclic Graph (DCG)

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.2.0

----



### [REQ]  Conditional Branching in Workflow
The SDK shall support conditional & dynamic activation of an Operator in an Application at run-time

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.2.0

---

### [REQ]  Support for Classification
The SDK shall support designing operator that perform classification with an ML/DL based model

#### Background
TBD

#### Verification Strategy
TBD
#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ]  Support for Segmentation
The SDK shall support designing operator that perform segmentation with an ML/DL based model

#### Background
TBD


#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ]  Support for general purpose computation
The SDK shall support developing operator that performs custom computation 

#### Background
TBD


#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ]  Supporting PyTorch as a DL Framework
The SDK shall enable incorporating model trained with PyTorch as an ingredient to be used for an Inference operator

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] Supporting TensorFlow as a DL Framework
The SDK shall enable incorporating model trained with Tensorflow as an ingredient to be used for an Inference operator

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] Supporting MMAR
The SDK shall allow integration of a Clara Train (MONAI core) generated MMAR in an operator
Usage of Triton

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] Supporting Triton
The SDK shall allow designing operators which can use Triton for inference
DICOM Networking Protocol

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0


### [REQ]  Supporting DICOM as a networking protocol
The SDK shall enable applications to integrate with medical informatics data source & sinks using DICOM as a networking protocol.

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---


### [REQ] Parsing a collection of DICOM series
The SDK shall enable filtering a set of DICOM Series with user defined parsing criteria expressed in terms of a collection of keys-value pairs where each key represents a DICOM Attribute

#### Background
TBD


#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---


### [REQ] Loading imaging dataset from DICOM Part 10 files or stored messages
The SDK shall enable applications to load 2D/3D imaging dataset represented by a DICOM series as an input to an operator used by an application

#### Background
TBD


#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] Supporting DICOM Segmentation  Storage SOP
The SDK shall provide an operator that supports exporting a Segmentation Storage SOP Instance. This operator shall be able to output a multi-frame image representing a classification of pixels in one or more referenced images. Segmentations are either binary or fractional.

#### Background
TBD


#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---


### [REQ] Supporting DICOM RT Structure  Storage SOP Instance
The SDK shall provide an operator that supports exporting a RT Structure Set Storage SOP Instance.

#### Background
TBD


#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] GPU Accelerated Primitives
The SDK shall allow support for incorporating common GPU accelerated image processing and computer vision primitives in an Operator
App Verification

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---


### [REQ] App Verification
The SDK shall enable app verification at two levels: operator, application

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] App Analytics
The SDK shall allow analyzing performance of the application at multiple levels: application, operator, kernel

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.2.0

---


### [REQ] Data Visualization
The SDK shall enable 2D/3D/4D medical image visualization of input, intermediate artifacts & output of an application during development

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.2.0

---

### [REQ] Data Specification for App
The SDK shall enable developers to specify conditions so that the right input datasets can be routed to an app during execution

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---


### [REQ] App Resource Requirements

#### Background
TBD

The SDK shall enable developers to specify desired resource requirements (GPU Memory, System Memory), for the application during app development

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] Existing Containers
The SDK shall support use of an existing container image for designing an Operator

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0

---

### [REQ] Packaging an Application
The SDK shall allow packaging of the application in a standardized format so that it can be executed by a compliant runtime environment

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0



### [REQ]  Execution of Application
The SDK shall allow execution of an application in the developer's workstation.

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.1.0


### [REQ] Development Console
The SDK shall provide a Development Console to track activities during designing of an application

#### Background
TBD

#### Verification Strategy
TBD

#### Target Release
MONAI Deploy App SDK 0.2.0


