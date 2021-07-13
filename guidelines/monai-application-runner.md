# MONAI Appication Runner (MAR)

## Description

This is a proposal for the MONAI Deploy Working Group.

- [Overview](#overview)
  - [Goal](#goal)
  - [Standard Language](#standard-language)
- [Requirements](#requirements)
  - [Supported MONAI Deploy Operating Environments](#supported-operating-environments)
  - [Input Requirements](#input-requirements)
  - [Associate input and output with MAP](#associate-input-and-output-with-map)
  - [One MAP at a time](#one-map-at-a-time)
  - [Monitor application](#monitor-application)
  - [Resource provisioning](#resource-provisioning)
  - [Authentication and security](#authentication)
- [Architecture & Design](#architecture--design)
  - [Description](#description)
  - [Arguments](#arguments)

## Overview

As data scientists & app developers build AI models and create MONAI Application Package (MAP) to deploy these apps in Production, they SHALL need a way to test their MAP locally without having to setup MONAI Deploy App Server and deploy MAP in the server. MONAI Application Runner (MAR) will be used to run and test MAP, one at a time, in the supported operating environment. This proposal documents the specifications for MAR.

### Goal
The goal for this proposal is to enlist and provide clarity on the specifications for MAR. Developers working on different software modules in MAR SHALL use this specification as a guideline when designing and implementing the MAR.

### Standard Language

This document SHALL follow the guidance of [rfc2119](https://datatracker.ietf.org/doc/html/rfc2119) for terminology.

## Requirements

### Supported MONAI Deploy Operating Environments

MAR SHALL be designed for Workstation environment.

See [MONAI Operating Environments](monai-operating-environments.md) for additional information about environments.

### Input Requirements

MAR SHALL be able to run specific MAP types as defined in [MONAI Application Package](./monai-application-package.md).

### Associate input and output with MAP

MAR SHALL allow users to map input and output local file or folder to their MAP input and output for execution.

### One MAP at a time

MAR SHALL execute a single MAP at a time.

### Monitor application progress, completion and failures

MAR SHALL track MONAI application execution progress, completion, and failures.

MAR SHOULD allow users to export the stdout and stderr from a running MONAI application.

### Resource provisioning

MAR SHALL NOT manage resources (CPU, GPU, and memory) for MONAI Applications.

### Authentication and security

MAR SHALL run as the user who runs it. MAR SHALL not provide authentication and security.

## Design and Architecture

### Description

The MONAI Application Runner (MAR) allows users to run and test their MONAI Application Package (MAP) locally. MAR allows the users to specify input and output path on local file system which it maps to the input and output of MAP during execution.

### Arguments

MAR SHALL have following arguments as positional arguments:

| Name     | Format                           | Description                                                   |
| -------- | -------------------------------- | ------------------------------------------------------------- |
| MAP      | `container-image-name[:tag]`     | MAP container image name with or without image tag.           |
| input    | file or directory path           | Local file or folder that contains input dataset for the MAP. |
| output   | path                             | Local path to store output from the executing MAP.            |

MAR SHOULD have following arguments as optional arguments:

| Name                | Shorthand  | Default    | Description                                                         |
| ------------------- | ---------- | ---------- | --------------------------------------------------------------      |
| quiet               | -q         | False      | Execute MAP quietly without printing container logs onto console.   |