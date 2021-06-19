# MONAI Deploy Application Server Specification

## Description
This is a proposal for the MONAI Deploy Working Group for the MONAI Deploy Application Server.

## Overview
As data scientists & app developers build AI models they need a way to deploy these apps in production. MONAI Deploy Application Server will be used to deploy multiple  MONAI applications. This proposal documents the requirements for MONAI Deploy Application Server.

## Goal
The goal for this proposal is to enlist, prioritize and provide clarity on the requirements for MONAI Deploy Application Server. Developers working on different software modules in MONAI Deploy Application Server SHALL use this specification as a guideline when designing and implementing software for the MONAI Deploy Application Server.

## Standard Language
This document SHALL follow the guidance of [rfc
2119](https://datatracker.ietf.org/doc/html/rfc2119) for terminology.

## Success Criteria
Users SHALL be able to communicate with the MONAI Application Server over the network with an API request. Users SHALL be able to register [MONAI Application Packages(MAP)](./monai-application-package.md) with the Application Server. Users SHALL be able to submit a job request to the Application Server for running a job corresponding to a MAP along with an input dataset. At a given time, multiple jobs can be run, depending on the system resources in the machine. On completion of jobs, results SHALL be made available to the users.

## Requirements

### Support for Specific MONAI workloads
The Application Server should be able to support specific versions of MONAI workloads as defined in [MONAI Workloads](./MONAI-Workloads.md).

The Application Server should be able to run specific MAP types as defined in [MONAI Application Package](./monai-application-package.md).

### Deployable on MONAI Operating Environments
MONAI Deploy Application Server SHALL run on MONAI Staging Server and MONAI Production Server environments as defined in [MONAI Operating Environments](./MONAI-Operating-Environments.md).

### Register and unregister MONAI applications
Application Server SHALL allow users to register and unregister MONAI applications.

### Maintain associations between input datasets and MONAI applications
Application Server SHALL maintain associations made by users between input datasets and MONAI applications.

### Run MONAI applications with associated datasets
Application Server SHALL run MONAI applications with selected input dataset.

### Provision resources for applications
Application Server SHALL provision CPU, memory, and GPU resources for applications.

### Monitor and report MONAI application job progress, completion and failures
Application Server SHALL track and report MONAI application job progress, and detect completion and failures.

### Notify registered job handler about job completion
Application Server SHALL notify registered job handler about job completion.

### Provide results of completed jobs
Application Server SHALL provide results of completed jobs.

## Design and Architecture

### API Spec
App Server SHALL expose the following APIs

#### Register MAP
This API SHALL allow users to register a MAP with the App Server.

#### Unregister MAP
This API SHALL allow users to unregister a MAP with the App Server. When a MAP is unregistered, users SHALL not be able to run a job for that MAP.

#### List MAPs
This API SHALL allow users to list available MAPs.
Unregistered MAPs SHALL not appear in the list of MAPs.

#### Describe MAP
This API SHALL allow users to get all the information pertaining to a MAP.

#### Upload Dataset
This API SHALL allow users to upload a dataset to the Application Server.

#### Run a Job for Dataset and MAP combination
This API SHALL allow users to run a job corresponding to a registered MAP and uploaded dataset.

#### Get Job Status
This API SHALL allow users to get the status of a job.

#### Download results for Job
This API SHALL allow users to download the results of a job.

#### Register Notification Handler
This API SHALL allow users to register a notification handler. Application Server SHALL post job completion events to registered notification handlers.

#### Unregister Notification Handler
This API SHALL allow users to unregister a notification handler. Once a notification handler has been unregistered, Application Server SHALL NOT post job completion events to notification handlers.

#### Cleaning up results for completed job
This API SHALL allow users to delete the results of a completed job.

#### List jobs
This API SHALL allow users to list all jobs.

#### Finalize job
This API SHALL allow users to finalize a job, allowing the Application Server to then cleanup the outputs for the job.

### Job Lifecycle in Production

- User registers MAP with Server.
- Server extracts manifest from MAP.
- PACs uploads data to Router.
- Router determines which MAP to run with dataset.
- Router requests Server to run a job with given dataset and chosen MAP.
- Server provisions resources for job.
- Server launches job.
- Server monitors job.
- Server detects job completion.
- Server releases resources held by job.
- Server notifies handler of job completion.

