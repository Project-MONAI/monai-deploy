# MONAI Application Runner (MAR)

## Description

- [Overview](#overview)
  - [Goal](#goal)
- [Requirements](#requirements)
  - [Supported MONAI Deploy Operating Environments](#supported-operating-environments)
  - [Input Requirements](#input-requirements)
  - [Associate input and output with MAP](#associate-input-and-output-with-map)
  - [One MAP at a time](#one-map-at-a-time)
  - [Monitor application](#monitor-application)
  - [Authentication and security](#authentication)
- [Architecture & Design](#architecture--design)
  - [Description](#description)
  - [Arguments](#arguments)

## Overview

As data scientists & application developers build AI models and create [MONAI Application Packages (MAPs)](./monai-application-package.md) to deploy these applications in production, they SHALL need a way to test their MAP locally without having to setup [MONAI Deploy Application Server](./application-server.md) and deploy MAPs in the server. MONAI Application Runner (MAR) will be used to run and test MAPs, one at a time, in the supported operating environment. This proposal documents the specifications for MAR.

### Goal

The goal for this proposal is to enlist and provide clarity on the specifications for MAR. Developers working on different software modules in MAR SHALL use this specification as a guideline when designing and implementing the MAR.

## Requirements

### Supported MONAI Deploy Operating Environments

MAR SHALL be designed for a Workstation environment as defined in [MONAI Operating Environments](./monai-operating-environments.md).

### Input Requirements

MAR SHALL be able to run specific MAP types as defined in [MONAI Application Package](./monai-application-package.md).

### Associate input and output with MAP

MAR SHALL allow users to map input and output local file or folder to their MAP input and output for execution.

### One MAP at a time

MAR SHALL execute a single MAP at a time.

### Monitor application progress, completion and failures

MAR SHALL track MONAI application execution progress, completion, and failures.

MAR SHOULD allow users to export the stdout and stderr from a running MONAI application.

### Authentication and security

MAR SHALL run as the user who runs it. MAR SHALL NOT provide authentication and security.

## Design and Architecture

### Description

The MONAI Application Runner (MAR) allows users to run and test their MONAI Application Packages (MAPs) locally. MAR allows the users to specify input and output path on local file system which it maps to the input and output of MAP during execution.

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
