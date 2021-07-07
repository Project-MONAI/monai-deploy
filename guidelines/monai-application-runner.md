# MONAI Appication Runner (MAR) Requirements

## Description
This is a proposal for the MONAI Deploy Working Group.

## Overview
As data scientists & app developers build AI models and create MONAI Application Package (MAP) to deploy these apps in Production, they SHALL need a way to test their MAP locally without having to setup MONAI Deploy App Server and deploy MAP in the server. MONAI Application Runner (MAR) will be used to run and test MAP, one at a time, in the supported operating environment. This proposal documents the requirements for MAR.

## Goal
The goal for this proposal is to enlist and provide clarity on the requirements for MAR. Developers working on different software modules in MAR SHALL use this specification as a guideline when designing and implementing the MAR.

## Standard Language
This document SHALL follow the guidance of [rfc2119](https://datatracker.ietf.org/doc/html/rfc2119) for terminology.

## Requirements

### Supported MONAI Deploy Operating Environments
MAR SHALL be designed for Workstation environment.

See [MONAI Operating Environments](monai-operating-environments.md) for additional information about environments.

### Input requirements
MAR SHALL be able to run specific MAP types as defined in [MONAI Application Package](./monai-application-package.md).

### Associate input and output with MAP
MAR SHALL allow users to map input and output local file system folders to their MAP input and output for execution.

### One MAP at a time
MAR SHALL execute a single MAP at a time.

### Monitor application progress, completion and failures
MAR SHALL track MONAI application execution progress, completion, and failures.

MAR SHALL provide an option to export the stdout and stderr from a running MONAI application.

### Resource provisioning
MAR SHALL NOT manage resources (CPU, GPU, and memory) for MONAI Applications.

### Authentication and security
MAR SHALL not provide authentication and security. MAR SHALL run as the user who runs it.
