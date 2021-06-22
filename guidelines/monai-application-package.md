# MONAI Application Package

## Description

This is a proposal for the MONAI Deploy Working Group.


## Overview

This proposal documents the guidelines of the first version of the MONAI Application Package (MAP).

> [Note]
> These guidelines are non-optional. Non-conformance to guidelines will make a package incompatible with MAP.


## Goal

The goal of this proposal is to provide structure of a MAP, define the purpose of a MAP and how it can be
interacted with, and the required and optional components of a MAP.


## Requirements

The following are requirements which need to be met by the MAP specification to be considered complete and approved.


### Contains an Application

A MAP SHALL contain an executable application which.


### Minimal Number of Artifacts

A MAP SHALL be comprised of a minimal number of artifacts. The ideal would be for a MAP to be single, self-describing artifact.


### Description

A MAP MUST be describable in a manner which facilitates deployment in a machine readable format.

The method of description SHALL be declarative and immutable.

The method of description SHALL provide the following information about the MAP:

- Execution requirements such as dependencies, restrictions, etc.
- Input and output data details such as data formats, modalities, and other protocols.
- Resource requirements such as CPU cores, available system memory, GPU availability, etc.


### Local Execution

A MAP MUST be in a format which support local execution in a development environment.

> [Note]
> See [MONAI Operating Environments](monai-operating-environments.md) for additional information about supported environments.


### Compatible with Kubernetes

A MAP SHALL NOT be in a format which inhibits or hampers the ability to deploy it using Kubernetes. This means at least a portion of the MAP needs to be a containerized application.


### Facilitate GPU Acceleration

A MAP SHALL enable applications to be developed with GPU acceleration.

