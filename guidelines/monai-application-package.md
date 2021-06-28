# MONAI Application Package

## Description

This is a proposal for the MONAI Deploy Working Group.


## Overview

This proposal documents the specification of the initial version of the MONAI Application Package (MAP).


## Goal

The goal of this proposal is to provide structure of a MAP, define the purpose of a MAP and how it can be
interacted with, and the required and optional components of a MAP.


## Requirements

The following are requirements which need to be met by the MAP specification to be considered complete and approved.


### Contains an Application

A MAP SHALL contain an executable application which supports the primary function of the MAP, and provide sufficient information to execute the application as intended.


### Minimal Number of Artifacts

A MAP SHALL be comprised of a single container which meets the minimum requirements set forth by this document.


### Describable

A MAP MUST be describable in a manner which facilitates deployment in a machine readable format.

The method of description SHALL be declarative and immutable.

The method of description SHALL provide the following information about the MAP:

- Execution requirements such as dependencies, restrictions, etc.
- Resource requirements such as CPU cores, available system memory, GPU availability, etc.

### Describe Inputs/Outputs

A MAP SHALL provide information about its expected inputs such that an external agent is able to determine if the MAP is capable of receiving a workload.

A MAP SHALL provide sufficient information about its outputs that an external agent is able to determine if it is capable of receiving the results.

### Local Execution

A MAP MUST be in a format which support local execution in a development environment.

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


# Architecture & Design

## Description

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
> The format and schema of the Application Manifest has not defined as part of this document.
> These items are suggested, but not part of any specification yet.

- Application Manifest MUST define the command used to run the Application (`/etc/monai/app.json#command`).
- Application Manifest SHOULD define input path used by the Application (`/etc/monai/app.json#input.path`).
- Application Manifest SHOULD define input data formats supported by the Application (`/etc/monai/app.json#input.formats`).
- Application Manifest SHOULD define output path used by the Application (`/etc/monai/app.json#output.path`).
- Application Manifest SHOULD define output data format produces by the Application (`/etc/monai/app.json#output.format`).
- Application Manifest SHOULD define any timeout applied to the Application (`/etc/monai/app.json#timeout`).
- Application Manifest MUST enable the specification of environment variables for the Application (`/etc/monai/app.json#environment`)
- _other features or requirements of the Application <!__AI__: @MMelQin!>


### Package Manifest

Provides information about the MAP's package layout. Not intended as a mechanism for controlling how the MAP is used or how the MAP's application is executed.

> [!IMPORTANT]
> The format and schema of the Package Manifest has not defined as part of this document.
> These items are suggested, but not part of any specification yet.

- Package Manifest MUST be UTF-8 encoded and use the JavaScript Object Notation (JSON) format.
- Package Manifest MUST indicate the MONAI framework version used to create the MAP (`/etc/monai/pkg.json#sdk-version`).
- Package Manifest SHOULD support either CRLF and LF style line endings.
- Package Manifest MUST specify the folder which contains the Application.
- Package Manifest SHOULD list the models used by the application (`/etc/monai/pkg.json#models`).
  - Models SHALL be defined by name.
  - Models SHOULD have a local path if they're included in the MAP itself.
  - Models SHOULD be in sub-folders of the `/var/opt/monai/models/` folder.
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


### Manifest Export

The Executor is able to function in a special mode in which it will export the MAP's manifest files to a mounted folder. This enables external tooling and services to read the manifest without any special tooling beyond the ability to run the MAP correctly.

The Executor MUST detect `/var/run/monai/export/` is mounted. When detected, the Executor SHALL copy `/etc/monai/app.json` and `/etc/monai/pkg.json` to `/var/run/monai/export/` and exit, instead of running the application.

When the Executor performs a manifest export, it SHALL NOT invoke the Application.


### Visualization

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

| Path                       | Purpose                                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------------- |
| `/etc/monai/`              | MAP manifests and immutable configuration files.                                               |
| `/etc/monai/app.json`      | Application Manifest file.                                                                     |
| `/etc/monai/pkg.json`      | Package Manifest file.                                                                         |
| `/opt/monai/app/`          | Application code, scripts, and other files.                                                    |
| `/opt/monai/executor/`     | Executor binaries.                                                                             |
| `/var/opt/monai/models/`   | AI models. Each model should be in a separate sub-folder.                                      |
| `/var/run/monai/export/`   | Special case folder which causes the Executor to copy all manifest to the folder when present. |

