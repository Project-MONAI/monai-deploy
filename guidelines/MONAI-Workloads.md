# MONAI Deploy Workloads

A number of workloads could be addressed by the MONAI deploy SDK and
framework. This document outlines how we will categorize a
workload. How to think about it from a deployment point-of-view. We
will use these definitions to outline the requirements for deployment
infrastructure.

## Standard Language
This document SHALL follow the
guidance of rfc 2119 for terminology.

## Definitions:

- **Job:** when you request the computing resources to accomplish a specific
task, that is called a “job”.

- **Synchronous jobs:** this is a job that MUST run immediately. It MAY
interact with humans or peripherals as needed.  Asynchronous jobs:
these are jobs SHALL be scheduled to be run when resources are
available.

- **Timeout:** asynchronous jobs MAY be submitted with a timeout specified
such that they MUST be scheduled within the timeout or they will be
marked as failed. This is another way of representing a required
service-level-agreement (SLA) necessary for the workload.

- **Throughput:** This is the measure of the number of jobs that can be
processed by specified hardware/software configuration over a specific
period of time.

- **Deterministic service requirements:** this is where the
containers and services required to complete the job are known before
the job is scheduled.

- **Cyclic service requirements:** this is where, to
complete the job, the container or containers may be executed in a
cycle or manner where they are re-entrant for the job.

- **Non-deterministic service requirements:** this is where the containers
and services required to complete the job are not known before the job
is scheduled and are determined during the execution of the job.

- **Latency:** is the measurement of time between the job being requested
and initial results returned.

## Workloads Considered

### Trauma / Emergency Case

Immediate diagnostics required for emergency care: immediate
processing is required for a clinical diagnosis of the trauma. These
workloads have the patient either awaiting further imaging or
diagnostics. Seconds count for some emergency diagnostics situations
(such as stroke).

- Example: Evaluation of Brain Injury in MR/ The typical data size: is
500 slices / series; 512 x 512 / slice; 16 bits / pixel, Today, the
typical response time is less than 10 minutes.
  - This is a case where you have a workload that typically could be done
asynchronously but now MUST be executed synchronously.

### Scheduled Radiology Workflows

These are often analyzed asynchronously: multiple images/studies are
analyzed for scheduled clinical studies, research or pro-active
diagnostics. Typically, in a clinical setting, the imaging has been
scheduled and the patient will arrive at a predictable time so
workload can be forecasted.

- Example: Evaluation of Liver in CT; The typical Data Size: 1000 - 2000
slices in a series; 512 x 512 / slice; 16 bits / pixel. Today, the
typical response time is greater than 30 minutes.
- Example: Retrospective analysis over multiple and related data sets
- Example: existing CT scans could be analyzed when new applications,
algorithms, or models are available. This would repeat the previous
example over many patients (100s to 1000s).
  - This is an example of an asynchronous job that may have a timeout
measured in tens of minutes.


### Quality Verification
Help the radiology technician improve their results.

- Example: Is it a good mammogram? The typical data size: 2048×2048 /
image; 12 bits / pixel; the typical response time today is < 2 minutes

- Example: Metadata Quality Assurance : validating the usability of an
image or data. Does the metadata associated with an image match the
image? For instance, is this a left or right femur? The label states
one direction but the image suggests another.

- Example: does the scan need to be repeated? Did the patient move while
the scan was being made?

### Image Enhancement:
Using computation and AI techniques, clarify the image for human and machine analysis.

### Medical Text Analysis:

Natural language recognition used with medical notes producing coding
and diagnostic assistance. For instance, validate that the medical
regime is both safe and effective for this patient given known medical
history.

### AI Assisted Labeling (MONAI Label):
AI assisted labeling is part of the training workflow. MONAI labeling
assists a human trainer by suggesting areas to be labeled by
inference. As training progresses, models may be updated for the
inference engine.

### Speech Based Medical Coding:
Using natural language recognition, transcribe and code the clinical notes.

## Workloads Out of Scope
For the purpose of this document, the following workloads are out of scope:

- Genomic Sequence Analysis :
- Drug Discovery :
- Training :
- MONAI Stream : MONAI stream applications. Inference workloads that
  are being run over live streams of images. An example application
  would be ultrasound guided medical operations in a clinical
  setting. This is a highly latency sensitive workload with immediate,
  synchronous response expected. We expect that the analysis will need
  to take less than 100ms in order to be useful.

