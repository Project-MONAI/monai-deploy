# High Level Requirements for MONAI Application Development SDK

## Designing Application
Enable developing applications that can leverage ML/DL/Computer Vision models to perform inference

## DAG Based Representation
Enable designing application workflows which can be represented by a Directed Acyclic Graph (DAG)

> (@whoisj) If a MONAI Application Package [MAP] is a single container, and we're expecting developer to write the application to be containerized using Python w/ MONAI libaries, then does this need to stated? Isn't this a function of Python itself?
> (@rahul-imaging) Application Developers need help in structuring their healthcare applications that make use of ML/DL/CV models. This requirement is addresseing how during design time a workflow can be & should be represented. The fact that it will be exported in a single container for deployment has nothing to do with it. In future the MONAI App Package may support multiple containers at deploy-time. Our app developers would still need a way to structure their workflow in Python code

## DCG Based Representation
Enable designing application workflows which can be represented by a Directed Cyclic Graph (DCG)

> (@whoisj) If a MONAI Application Package [MAP] is a single container, and we're expecting developer to write the application to be containerized using Python w/ MONAI libaries, then does this need to stated? Isn't this a function of Python itself?

## Conditional Branching
Support conditional and dynamic activation of an Operator in an Application at run-time

> (@whoisj) If a MONAI Application Package [MAP] is a single container, and we're expecting developer to write the application to be containerized using Python w/ MONAI libaries, then does this need to stated? Isn't this a function of Python itself?

## Support for basic ML Inference Operations
Support designing operators that perform common ML/DL tasks such as classification, segmentation, ROI detection in 2D and 3D

## Support for common model types
Enable incorporating custom trained model (PyTorch, TensorFlow, Caffe) as part of an operator

## Integration of MMAR
Allow integration of a Clara Train generated MMAR in an operator

## Inference with Popular DL Frameworks
Allow designing operators which can use a DL framework for inference: PyTorch, TensorFlow, Caffe

## Enabling Triton for Inference
Allow designing operators which can use Triton for inference

## Integration with Informatics Data Sources and Sinks
Enable applications to integrate with medical informatics data source and sinks (DICOM Messages, DICOM Part 10, FHIR)

## Supporting GPU Accelerated Image Processing and Computer Vision
Allow support for incorporating common GPU accelerated image processing and computer vision primitives in an Operator

## Ability to Verify an Application
Enable app verification at two levels: operator, application 

> (@whoisj) Is an “operator” a “function” or a “container”? I was under the impression that operators were SDK provided objects / functions, not containers. If they are objects / functions, how does verification work? Or, maybe by “verification” you mean “test”? Sorry, rather confused.

## App Analytics
Allow analyzing performance of the application at multiple levels: application, operator, kernel

> (@whoisj) I think would be pertinent to include GPU/CUDA here as well.

## Visualization for the Purpose of Debugging App
Enable 2D/3D/4D and time series-based visualization of input, intermediate artifacts, and output of an application during development

## Discovering Right Application Routing Data
Enable developers to specify conditions so that the right input datasets can be routed to the correct app during execution

> (@whoisj) While I appreciate the idea behind this, I’m not to which component or SDK provided tool this would apply. Please elaborate.

## Specifying Resources for Operators
Allow developers to specify desired resource requirements (CPU, GPU, System Memory), for an operator during app development

> (@whoisj) If the MONAI Application Package is a single containerized application, does it make sense for individual operators (aka SDK functions) to have resource requirements?

## Ability to Utilize an Existing Container
Support use of an existing container image for designing an operator

> (@whoisj) This needs more elaboration. Not sure I can accept this as a requirement when I do not even understand what it means. I thought “operators” were functions provided by the proposed MONAI SDK, here it sounds like an operator is a container unto itself.

## Packaging an Application
Allow packaging of the application in a standardized format so that it can be executed by a compliant runtime environment

## Executing an Application
Allow execution of an application on developer’s workstation.

## Development Console
Provide a development console to track activities during designing of an application

### Comments & Questions

(@whoisj) I do not see the ability to debug the application in this list, perhaps I missed it.
Additionally, I’d like to see the requirement that a MONAI Application Package MAP can be run via the Application Runner or Server without modification as a requirement.
