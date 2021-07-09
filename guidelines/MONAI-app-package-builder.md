# MONAI Application Package Builder

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
  - [Builder Specification](#builder-specification)
    - [Building MAP with MONAI Application](#building-map-with-monai-application)
    - [Building MAP from existing container](#building-map-from-existing-container)

## Overview
Data scientists and application developers will require a utility to package their MONAI applications into deployable MONAI Application Packages (MAP). This proposal documents the specification of the initial version of the MONAI Application Package Builder (Builder).

### Goal

The goal of this proposal is to achieve clarity on the initial  structure of the Builder, with regards specifically to how it should create a deployable package and the interface it should provide to users.

##  Requirements

The following are requirements which need to be met by the MAP Builder specification to be considered complete and approved.

### Creates Deployable Single Container

Builder SHALL produce a functional MAP which SHALL be a deployable single containerized application

### Packages Required MAP Components

Builder SHALL package/provide all required components specified in [MONAI Application Package](./monai-application-package.md). 

### Offers Intuitive Interface

Builder SHOULD provide users with an intuitive interface to package an application into a MAP.

Builder SHOULD provide a command-line interface for users to package an application into a MAP.

### Input Requirements

Users SHALL provide the Builder a MONAI application along with any optional pre-trained models to be packaged into a MAP. 

### Converting Existing Images

Builder SHALL support converting existing container images into MAPs

## Architecture & Design

Builder SHALL accept a user supplied application and package it into a MAP

[!IMPORTANT]
The full design and layout for a MAP produced by Builder can be found in the [MONAI Application Package](./monai-application-package.md) design document.

### Builder Specification

Builder SHALL adhere to the MAP specification when building a MAP

Builder SHALL be a client that supports the following features

#### Building MAP with MONAI Application

Builder SHALL support building a MAP with a user supplied MONAI application and any optional pre-trained models

#### Building MAP from existing container

Builder SHALL support building a MAP from an existing container
