# MONAI Appication Runner Requirements #

## Description
This is a proposal for the MONAI Deploy Working Group.

## Overview ##
As data scientists & app developers build AI models and create MONAI App Package (MAP) to deploy these apps in Production, they SHALL need a way to test their MAP locally without having to setup MONAI Deploy App Server and deploy MAP in the server. MONAI Application Runner will be used to deploy MONAI applications, one at a time, in the supported operating environment. This proposal documents the requirements for MONAI Application Runner.

## Goal ##
The goal for this proposal is to enlist and provide clarity on the requirements for MONAI Application Runner. Developers working on different software modules in MONAI Application Runner SHALL use this specification as a guideline when designing and implementing the MONAI Application Runner.

## Standard Language ##
This document SHALL follow the guidance of [rfc2119](https://datatracker.ietf.org/doc/html/rfc2119) for terminology.

## MONAI Application Runner Requirements ##

### Supported MONAI Operating Environments ###
MONAI Application Runner SHALL be designed for Desktop and Workstation environments.

See [MONAI Operating Environments](monai-operating-environments.md) for additional information about environments.

### Input requirements ###
The MONAI Application Runner should be able to run specific MAP types as defined in [MONAI Application Package](./monai-application-package.md).

### Associate input datasets with MONAI applications
MONAI Application Runner SHALL allow users to specify input datasets for their MONAI application.

### One MONAI application at a time ###
MONAI Application Runner SHALL run one MONAI application at a time.

### Monitor application progress, completion and failures ###
MONAI Application Runner SHALL track MONAI application job progress, and detect completion and failures.

### Resource provisioning ###
MONAI Application Runner SHALL NOT manage resources (GPU, CPU and memory) for MONAI Applications.

### Authentication and security ###
MONAI Application Runner SHALL not support authentication and security.
