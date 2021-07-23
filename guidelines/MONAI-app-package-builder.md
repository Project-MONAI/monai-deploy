# MONAI Application Packager

## Description

This is a proposal for the MONAI Deploy Working Group.

- [Overview](#overview)
  - [Goal](#goal)
- [Requirements](#requirements)
  - [Creates Deployable Single Container](#creates-deployable-single-container)
  - [Packages Required MAP Components](#packages-required-map-components)
  - [Offers Intuitive Interface](#offers-intuitive-interface)
  - [Input Requirements](#input-requirements)
  - [Converting Existing Images](#converting-existing-images)
- [Architecture & Design](#architecture--design)
  - [Packager Specification](#packager-specification)
    - [Packaging MAP with MONAI Application](#packaging-map-with-monai-application)
    - [Packaging MAP from existing container](#packaging-map-from-existing-container)

## Overview
Data scientists and application developers will require a utility to package their MONAI applications into deployable MONAI Application Packages (MAP). This proposal documents the specification of the initial version of the MONAI Application Packager (Packager).

### Goal

The goal of this proposal is to achieve clarity on the initial  structure of the Packager, with regards specifically to how it should create a deployable package and the interface it should provide to users.

##  Requirements

The following are requirements which need to be met by the MAP Packager specification to be considered complete and approved.

### Creates Deployable Single Container

Packager SHALL produce a functional MAP which SHALL be a deployable single containerized application

### Packages Required MAP Components

Packager SHALL package/provide all required components specified in [MONAI Application Package](./monai-application-package.md). 

### Offers Intuitive Interface

Packager SHOULD provide users with an intuitive interface to package an application into a MAP.

Packager SHOULD provide a command-line interface for users to package an application into a MAP.

### Input Requirements

Packager SHALL take a MONAI Application and any optional pre-trained models as input.

### Converting Existing Images

Packager SHALL support converting existing container images into MAPs

## Architecture & Design

Packager SHALL accept a user supplied application and package it into a MAP

[!IMPORTANT]
The full design and layout for a MAP produced by Packager can be found in the [MONAI Application Package](./monai-application-package.md) design document.

### Packager Specification

Packager SHALL adhere to the MAP specification when packaging a MAP

Packager SHALL be a client that supports the following features

#### Packaging MAP with MONAI Application

Packager SHALL support packaging a MAP with a user supplied MONAI application and any optional pre-trained models

#### Packaging MAP from existing container

Packager SHALL support packaging a MAP from an existing container
