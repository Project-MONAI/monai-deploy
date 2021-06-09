# High Level Requirements for MONAI Application Development SDK

## Designing Application
Enable developing applications that can leverage ML/DL/Computer Vision models to perform inference

## DAG Based representation
Enable designing application workflows which can be represented by a Directed Acyclic Graph (DAG)

## DCG Based representation
Enable designing application workflows which can be represented by a Directed Cyclic Graph (DCG)

## Coditional branching
Support conditional & dynamic activation of an Operator in an Application at run-time

## Support for basic ML Inference Operations
Support designing operators that perform common ML/DL tasks such as classification, segmentation, ROI detection in 2D & 3D

## Support for common model types
Enable incorporating custom trained model (PyTorch, TensorFlow, Caffe) as part of an operator

## Integration of MMAR
Allow integration of a Clara Train generated MMAR in an operator

## Inference wih popular DL frameworks
Allow designing operators which can use a DL framework for inference: PyTorch, TensorFlow, Caffe

## Enabling Triton for inference
Allow designing operators which can use Triton for inference

## Integration with Informatics Data Sources & Sinks
Enable applications to integrate with medical informatics data source and sinks (DICOM Messages, DICOM Part 10, FHIR)

## Supporting GPU Accelerated Image Processing & Computer Vision
Allow support for incorporating common GPU accelerated image processing and computer vision primitives in an Operator

## Ability to verify an App
Enable app verification at two levels: operator, application 

## App Analytics
Allow analyzing performance of the application at multiple levels: application, operator, kernel

## Visualization for the purpose of Debugging App
Enable 2D/3D/4D and time series based visualization of input, intermediate artifacts & output of an application during development

## Discovering right application  routing data
Enable developers to specify conditions so that the right input datasets can be routed to an app during execution

## Specifying resources for operators
Allow developers to specify desired resource requirements (GPU Memory, System Memory), for an operator during app development

## Ability to utilize an existing container
Support use of an existing container image for designing an Operator

## Packaging an Application
Allow packaging of the application in a standardized format so that it can be executed by a compliant runtime environment

## Executing and Application
Allow execution of an application in developer’s workstation.

## Development Console
Provide a Development Console to track activities during designing of an application