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

>(@rahul-imaging) Refer to my previous comment

## Conditional Branching
Support conditional and dynamic activation of an Operator in an Application at run-time

> (@whoisj) If a MONAI Application Package [MAP] is a single container, and we're expecting developer to write the application to be containerized using Python w/ MONAI libaries, then does this need to stated? Isn't this a function of Python itself?

> (@rahul-imaging) Here an Operator represents a logical "stage" in the application, not a container. Container is a deploy time concept. Refer to my previous comment

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

> (@rahul-imaging) An Operator a logical stage in a MONAI Application at design time. Whether a single design-time operator gets packaged into a single container or multiple operators get packaged into the same container is a deploy time concern. So far, the current thinking is that a logical Operator will be implemented as an instance of a Python class during application development. In addition, at least for the first release of MONAI Deploy, the entire application will be packaged into a single container.

## App Analytics
Allow analyzing performance of the application at multiple levels: application, operator, kernel

> (@whoisj) I think would be pertinent to include GPU/CUDA here as well.

> (@rahul-imaging) The "kernel" level analysis would include profiling GPU based implementation.

## Visualization for the Purpose of Debugging App
Enable 2D/3D/4D and time series-based visualization of input, intermediate artifacts, and output of an application during development

## Discovering Right Application Routing Data
Enable developers to specify conditions so that the right input datasets can be routed to the correct app during execution

> (@whoisj) While I appreciate the idea behind this, I’m not to which component or SDK provided tool this would apply. Please elaborate.
> (@rahul-imaging) How this requirement will be addressed in the design space, should be elaborated in an architecture document. Our general thinking so far is during application development, the user will make use of the SDK to provide a ser of rules to specify what kind of data is approproate for the app. Such rules can be based on DICOM header or FHIR resources, or the can be used on an algorithm (that may or may not use AI). 


## Specifying Resources for Operators
Allow developers to specify desired resource requirements (CPU, GPU, System Memory), for a application during app development

> (@whoisj) If the MONAI Application Package is a single containerized application, does it make sense for individual operators (aka SDK functions) to have resource requirements?

> (@rahul-imaging) Remember operator is a design-time concept. I made the requirement more generic none-the-less.

## Ability to Utilize an Existing Container
Support use of an existing container image for designing an operator

> (@whoisj) This needs more elaboration. Not sure I can accept this as a requirement when I do not even understand what it means. I thought “operators” were functions provided by the proposed MONAI SDK, here it sounds like an operator is a container unto itself.

> (@rahul-imaging) Several institues such as MGB already have pre-packaged containers (treated as black boxes) that contain an application which can perform all necessary steps given a set of inputs and generate outputs. Inputs/Outputs are often managed via mounted volumes. MONAI Deploy developers would need a way to bring those containers into their application development. The MONAI App SDK should provide a mechanism so that developers can make use of an existing container from their application. How this would be done should be described in the Architecture document.

## Packaging an Application
Allow packaging of the application in a standardized format so that it can be executed by a compliant runtime environment

## Executing an Application during development
Allow execution of an application on developer’s workstation.

## Executing an Application after deployment
Allow execution of an application in a deployed environment without any necessary modification

## Development Console
Provide a development console to track activities during designing of an application

### Comments & Questions

> (@whoisj) I do not see the ability to debug the application in this list, perhaps I missed it.
Additionally, I’d like to see the requirement that a MONAI Application Package MAP can be run via the Application Runner or Server without modification as a requirement.

> (@rahul-imaging) Requirement for "Executing an Application during development" was already there. I added another one for "Executing an Application after deployment"
