# MONAI Application Package

## Description

This is a proposal for the MONAI Deploy Working Group.

- [Overview](#overview)
  - [Goal](#goal)
  - [Assumptions](#assumptions)
- [Requirements](#requirements)
  - [Contains an Application](#contains-an-application)
  - [Single Artifact](#single-artifact)
  - [Self-Describing](#self-describing)
  - [IO Specification](#io-specification)
  - [Local Execution](#local-execution)
  - [Containerization](#containerization)
  - [Compatible with Kubernetes](#compatible-with-kubernetes)
  - [OCI Compliance](#oci-compliance)
  - [Facilitate GPU Acceleration](#facilitate-gpu-acceleration)
- [Architecture & Design](#architecture--design)
- [Description](#description)
- [Application](#application)
- [Manifests](#manifests)
  - [Application Manifest](#application-manifest)
  - [Package Manifest](#package-manifest)
- [Executor](#executor)
  - [Initial Conditions / Environment Variables](#initial-conditions)
  - [Manifest Export](#manifest-export)
  - [Layout Diagram](#layout-diagram)
- [Special Folders](#special-folders)


## Overview

This proposal documents the specification of the initial version of the MONAI Application Package (MAP).


### Goal

The goal of this proposal is to provide structure of a MAP, define the purpose of a MAP and how it can be
interacted with, and the required and optional components of a MAP.


### Assumptions

The following are a set of assumptions related to MAP execution, inspection, and general usage.

- Containerized applications will be based on Linux x86_64 (AMD64).

- Containerized application's host environment will be based on Linux x86_64 (AMD64) with container support.

- Developers expect local execution of their applications to behave identically to execution of the containerized version.

- Developers expect local execution of their containerized applications to behave identically to execution in deployment.

- Developers and operations engineers want the application packages to be self-describing.

- Application packages might not be developed using the MONAI Application SDK.

- Pre-existing, containerized applications will need to be "converted" into MONAI Application Packages.

- Application packages will be deployed in a variety of environments.

  > [Note]
  > See [MONAI Operating Environments](monai-operating-environments.md) for additional information about supported environments.


##  Requirements

The following are requirements which need to be met by the MAP specification to be considered complete and approved.


### Contains an Application

A MAP SHALL contain an executable application which supports the primary function of the MAP, and provide sufficient information to execute the application as intended.


### Single Artifact

A MAP SHALL be comprised of a single container which meets the minimum requirements set forth by this document.


### Self-Describing

A MAP MUST be self-describing and provide a mechanism for extracting the its description.

The method of description SHALL be a machine readable and writable format.

The method of description SHALL be a human readable format.

The method of description SHOULD be a human writable format.

The method of description SHALL be declarative and immutable.

The method of description SHALL provide the following information about the MAP:

- Execution requirements such as dependencies, restrictions, etc.

- Resource requirements such as CPU cores, available system memory, GPU availability, etc.


### IO Specification

A MAP SHALL provide information about its expected inputs such that an external agent is able to determine if the MAP is capable of receiving a workload.

A MAP SHALL provide information about the protocols and study types it supports such that an external agent is able to determine if the MAP is capable of receiving a workload.

A MAP SHALL provide sufficient information about its outputs that an external agent is able to determine if it is capable of receiving the results.


### Local Execution

A MAP MUST be in a format which supports local execution in a development environment.

> [Note]
> See [MONAI Operating Environments](monai-operating-environments.md) for additional information about supported environments.


### Containerization

A MAP SHALL be a containerized application to maximize portability of its application.


### Compatible with Kubernetes

A MAP SHALL NOT be in a format which inhibits or hampers the ability to deploy it using Kubernetes.


### OCI Compliance

The containerized portion of a MAP SHALL comply with [Open Container Initiative](https://opencontainers.org/) format standards.


### Facilitate GPU Acceleration

A MAP SHALL enable applications to be developed with GPU acceleration.

A MAP SHALL NOT impeded the adoption or utilization of accelerator (GPU) technology.


# Architecture & Design

##  Description

The MONAI Application Package (MAP) is a functional package designed to perform an action on datasets of a prescribed format. A MAP is a container image which adheres the specification provided in this document.


## Application

The primary component of a MAP is the Application. The Application is provided by an application developer and incorporated into the MAP using the MONAI Package Builder (Builder).

All application code and binaries SHALL be in the `/opt/monai/app/` folder, with the exception of any dependencies which are installed by the MONAI Application Package Builder during the creation of the MAP.

All AI models (PyTorch, TensorFlow, TensorRT, etc.) should be SHOULD be in separate sub-folders of the `/var/opt/monai/models/` folder.


## Manifests

A MAP SHALL contain two manifests: the application manifest and the package manifest. The package manifest shall be stored in `/etc/monai/pkg.json` and the application manifest shall be stored in `/etc/monai/app.json`. Once a MAP is created, it's manifests are expected to be immutable.


### Application Manifest

Provides information about the MAP's Application.

> [!IMPORTANT]
> The format and schema of the Application Manifest has not been defined as part of this document.
> These items are suggested, but not part of any specification yet.

- Application Manifest MUST define the command used to run the Application (`/etc/monai/app.json#command`).

  - When not provided the MAP will be considered invalid and not runnable by MONAI Deploy Application Runner and Server.

- Application Manifest SHOULD define the version of the manifest file schema (`/etc/monai/app.json#api-version`).

  - Manifest schema version SHALL be provided as a [semantic version](https://semver.org/) string.

- Application Manifest SHOULD define the version of the MONAI Deploy SDK used to create the Application (`/etc/monai/app.json#sdk-version`).

  - SDK version SHALL be provided as a [semantic version](https://semver.org/) string.

- Application Manifest SHOULD define the version of the Application itself (`/etc/monai/app.json#version`).

  - Application version SHALL be provided as a [semantic version](https://semver.org/) string.

- Application Manifest SHOULD define the Application's working directory (`/etc/monai/app.json#working-directory`).

  - The value provided must be an absolute path (first character is `/`).

  - When not provided the default path `/var/monai/` will be assumed.

- Application Manifest SHOULD define input path, relative to the working directory, used by the Application (`/etc/monai/app.json#input.path`).

  - The input path SHOULD be a relative file-system path to a directory or folder.

    - When the value is a relative file-system path (first character is not `/`), it is relative to the Application's working directory.

    - When the value is an absolute file-system path (first character is `/`), the file-system path is used as-is.

  - When not provided the default value `input/` will be used.

- Application Manifest SHOULD define input data formats supported by the Application (`/etc/monai/app.json#input.formats`).

- Application Manifest SHOULD define output path, relative to the working directory used by the Application (`/etc/monai/app.json#output.path`).

  - The input path SHOULD be a relative file-system path to a directory or folder.

    - When the value is a relative file-system path (first character is not `/`), it is relative to the Application's working directory.

    - When the value is an absolute file-system path (first character is `/`), the file-system path is used as-is.

  - When not provided the default value `output/` will be used.

- Application Manifest SHOULD define output data format produces by the Application (`/etc/monai/app.json#output.format`).

- Application Manifest SHOULD define any timeout applied to the Application (`/etc/monai/app.json#timeout`).

  - When not provided the default value `0` SHALL be assumed.

  - This value can be overridden by the top level executor, such as Application Server.

- Application Manifest MUST enable the specification of environment variables for the Application (`/etc/monai/app.json#environment`)


### Package Manifest

Provides information about the MAP's package layout. Not intended as a mechanism for controlling how the MAP is used or how the MAP's application is executed.

> [!IMPORTANT]
> The format and schema of the Package Manifest has not been defined as part of this document.
> These items are suggested, but not part of any specification yet.

- Package Manifest MUST be UTF-8 encoded and use the JavaScript Object Notation (JSON) format.

- Package Manifest SHOULD support either CRLF and LF style line endings.

- Package Manifest SHOULD specify the folder which contains the Application (`/etc/monai/pkg.json#app`).

  - When not provided the default path `/opt/monai/app/` will be assumed.

- Package Manifest SHOULD provide the version of the package file manifest schema (`/etc/monai/pkg.json#api-version`).

  - Manifest schema version SHALL be provided as a [semantic version](https://semver.org/) string.

- Package Manifest SHOULD provide the version of the tools used to build the package (`/etc/monai/pkg.json#sdk-version`).

  - SDK version SHALL be provided as a [semantic version](https://semver.org/) string.

- Package Manifest SHOULD provide the version of the package itself (`/etc/monai/pkg.json#version`).

  - Package version SHALL be provided as a [semantic version](https://semver.org/) string.

- Package Manifest SHOULD list the models used by the application (`/etc/monai/pkg.json#models`).

  - Models SHALL be defined by name (`/etc/monai/pkg.json#models[*].name`).

  - Models SHOULD provide a file-system path if they're included in the MAP itself (`/etc/monai/pkg.json#models[*].path`).

    - Model path SHOULD be relative to the folder containing the model.

    - When the model path is a relative file-system path (first character is not `/`), it is relative to the `/etc/monai/models/` folder.

    - When the model path is an absolute file-system path (first character is `/`), the file-system path is used as-is.

  - Models SHOULD be in sub-folders of the `/etc/monai/models/` folder.

- Package Manifest SHOULD specify the resources required to execute the application.

  This information is used to provision resources when running the application using the MONAI Application Server.

  - CPU requirements SHALL be denoted using decimal count of CPU cores (`/etc/monai/pkg.json#resources.cpu`).

  - GPU requirements SHALL be denoted using integer count of GPUs (`/etc/monai/pkg.json#resources.gpu`).

  - Memory requirements SHALL be denoted using decimal values followed by units (`/etc/monai/pkg.json#resources.memory`).

    - Supported units SHALL be megabytes (`Mi`) and gigabytes (`Gi`).

    - Example: `1.5Gi`, `2048Mi`

  - Integer values MUST be positive and not contain any position separators.

    - Example legal values: `1`, `42`, `2048`

    - Example illegal values: `-1`, `1.5`, `2,048`

  - Decimal values MUST be positive, rounded to nearest tenth, use the `.` character to separate whole and fractional values, and not contain any positional separators.

    - Example legal values: `1`, `1.0`, `0.5`, `2.5`, `1024`

    - Example illegal values: `1,024`, `-1.0`, `3.14`

  - When not provided the default values of `cpu=1`, `gpu=0`, and `memory=1Gi` will be assumed.


## Executor

The MAP Executor (Executor) provides a shim between the runner of a MAP and the MAP's application. Due to the Executor's shim nature, it can be extended beyond its original intent to provide additional functionality.

The Executor MUST be provided as part of the MONAI Application SDK.

The Executor SHALL be stored in the `/opt/monai/executor/` folder.

The Executor SHALL be the entry-point (or initial process) of a MAP's container.

The Executor SHALL, by default, execute the Application as defined by the Package Manifest and then exit.

The Executor SHALL set initial conditions for the Application when invoking it.

The Executor SHALL monitor the Application process and record its CPU, system memory, and GPU utilization metrics.

The Executor SHALL monitor the Application process and enforce any timeout value specified in `/etc/monai/app.json#timeout`.


### Initial Conditions

The Executor SHOULD provide a customized set of environment variables and command line options to the Application as part of invocation.

- The Executor MUST provide any environment variables specified by `/etc/monai/app.json#environment`.

- The Executor MUST provide the command line options specified by `/etc/monai/app.json#command`.

- The Executor MUST provide the following environment variables to the Application:

  - `MONAI_APPLICATION`: The path to the root of the Application.

    - The value is read from the Application Manifest (`/etc/monai/pkg.json#application.location`) by default.

  - `MONAI_HOSTNAME`: The name of the host running the MAP (default: `"none"`)

    - The value is expected to be a string.

    - Common values are `MONAI Application Runner` and `MONAI Application Server`.

  - `MONAI_HOSTVERSION`: The version of the host running the map (default: `0.0.`).

    - Host version SHALL be a [semantic 2.0 formatted](https://semver.org) string.

  - `MONAI_INPUTPATH`: The path to the folder where inputs can be expected to be read from (default: `/var/monai/input/`).

    - Input path SHALL be an absolute file-system path to a readable folder.

  - `MONAI_JOBID`: The unique identity of the job the MAP is being executed by (default: `"00000000000000000000000000000000`).

    - Job identifier SHALL be a string matching `/[A-F0-9a-f]{32}/`.

  - `MONAI_OUTPUTPATH`: The path to the folder where outputs are expected to written to (default: `/var/monai/output/`).

    - Output path SHALL be an absolute file-system path to a writable folder.

  - `MONAI_TIMEOUT`: The timeout, in seconds, being applied to the MAP (default: `0`).

    - Timeout SHALL be an integer number in the range of [`0`, `65536`].

    - A value of `0` SHALL indicate that no timeout is being applied to the Application.


#### Environment Variables

| Variable            | Default                                    | Format              | Description                                      |
| ------------------- | ------------------------------------------ | ------------------- | ------------------------------------------------ |
| `MONAI_APPLICATION` | `/etc/monai/pkg.json#application.location` | Folder Path         | Path to the Application.                         |
| `MONAI_HOSTNAME`    | `None`                                     | String              | Name of the host running the MAP.                |
| `MONAI_HOSTVERSION` | `0.0.0`                                    | Semantic Version    | Version of the host running the MAP.             |
| `MONAI_INPUTPATH`   | `/var/monai/input/`                        | Folder Path         | Path to the input folder for the Application.    |
| `MONAI_JOBID`       | `00000000000000000000000000000000`         | `/[A-F0-9a-f]{32}/` | Unique identity of the job the MAP is executing. |
| `MONAI_OUTPUTPATH`  | `/var/monai/output/`                       | Folder Path         | Path to the output folder for the Application.   |
| `MONAI_TIMEOUT`     | `/etc/monai/app.json#timeout`              | Integer             | Timeout, in seconds, applied to the Application. |


### Manifest Export

The Executor is able to function in a special mode in which it will export the MAP's manifest files to a mounted folder.
This enables external tooling and services to read the manifest without any special tooling beyond the ability to run the MAP correctly.

The Executor MUST detect when the following folders have been mounted.

- `/var/run/monai/export/app/`: when detected, the Executor will copy the contents of `/opt/monai/app/` to the folder.

- `/var/run/monai/export/config/`: when detected, the Executor will copy `/etc/monai/app.json` and `/etc/monai/pkg.json` to the folder.

- `/var/run/monai/export/models/`: when detected, the Executor will copy the contents of `/opt/monai/models/` to the folder.

- `/var/run/monai/export/`: when detected without any of the above being detected, the Executor SHALL:

  - copy the contents of `/opt/monai/app/` to `/var/run/monai/export/app/`.

  - copy `/etc/monai/app.json` and `/etc/monai/pkg.json` to `/var/run/monai/export/config/`.

  - copy the contents of `/opt/monai/models/` to `/var/run/monai/export/models/`.

When the Executor performs an export operation, it SHALL NOT invoke the Application.


## Layout Diagram

```
                        ╔═══════════════════════════════╗
  Added by Builder ---> ║ Executor │                    ║ <-- Developer code,
                        ╟──────────┤    Application     ║     probably Python,
  Created by Builder -> ║ Manifest │                    ║     using MONAI API.
                        ╟──────────┴────────────────────╢
                        ║            Model(s)           ║ <-- Optional pre-trained models.
                        ╚═══════════════════════════════╝
```


## Special Folders

| Path                            | Purpose                                                                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `/etc/monai/`                   | MAP manifests and immutable configuration files.                                                                  |
| `/etc/monai/app.json`           | Application Manifest file.                                                                                        |
| `/etc/monai/pkg.json`           | Package Manifest file.                                                                                            |
| `/opt/monai/app/`               | Application code, scripts, and other files.                                                                       |
| `/opt/monai/executor/`          | Executor binaries.                                                                                                |
| `/opt/monai/models/`            | AI models. Each model should be in a separate sub-folder.                                                         |
| `/var/monai/`                   | Default working directory.                                                                                        |
| `/var/monai/input/`             | Default input directory.                                                                                          |
| `/var/monai/output/`            | Default output directory.                                                                                         |
| `/var/run/monai/export/`        | Special case folder, causes the Executor to export contents related to the app. (see: [export](#manifest-export)) |
| `/var/run/monai/export/app/`    | Special case folder, causes the Executor to export the contents of `/opt/monai/app/` to the folder.               |
| `/var/run/monai/export/config/` | Special case folder, causes the Executor to export `/etc/monai/app.json` and `/etc/monai/pkg.json` to the folder. |
| `/var/run/monai/export/models/` | Special case folder, causes the Executor to export the contents of `/opt/monai/models/` to the folder.            |

