# MONAI Deploy Operating Environments #

This is a proposal for the MONAI Deploy Working Group.

## Overview ##

This proposal documents the different operating environments that are relevant
for deployment lifecycle from inception to production. The proposal introduces
workstation, development server, staging server, production server and cloud
environments as general environments where software development happens and it
tries to highlight the differences in quality and integration attributes that
are relevant to each of these environments.

## Goal ##

The goal for this proposal is to provide clarity on the similarities and
differences between the different operating environments where MONAI Deploy 
components are executed. Developers working on different software modules in 
MONAI MAY use this specification as a guideline when implementing software for
different use cases in different environments.  

## Standard Language ##

This document SHALL follow the guidance of [rfc
2119](https://datatracker.ietf.org/doc/html/rfc2119) for terminology.

## Environment Details ##

1. [Desktop/Laptop Environment](#desktoplaptop-environment)
2. [Workstation Environment](#workstation-environment)
3. [Development/Integration Server
Environment](#developmentintegration-server-environment)
4. [Staging Server Environment](#staging-server-environment)
5. [Production Server Environment](#production-server-environment)
6. [Cloud Environments](#cloud-environments)

### Desktop/Laptop Environment ###

A single user system, where a single developer or data scientist is using their
development tools and connecting to a remote, dedicated GPU workstation.

**Users:** Developers and data scientists.  

**Operating System:**  Typically Windows, Mac OSX where data scientists and
developers are running their development tools, accessing local data.  

**Hardware:**  System with minimum of 8GB RAM, 8 logical core, no GPU
in the minimum environment. CPU SHOULD be from the x86 family.

**Applications:**  Different tools include a mix of development tools, such as 
VS Code, and clinical research tools like JupyterLab, OHIF viewer, Python 
development environment and SSH for connecting to remote GPU workstation.  

**Security:** These environments fall under the institutional security 
requirements and it SHOULD be the responsibility of the individual developers 
to make sure those requirements are being met.


### Workstation Environment ###

A single user system, where a single developer or data scientist is doing most
of their development work either directly on the system or via a remote SSH
connection.

**Users:** Developers and data scientists.  

**Operating System:**  Typically a Linux environment, where data scientists and 
developers are running their development tools, accessing local data.  

**Hardware:**  Workstation with minimum of 8GB RAM, 8 logical core, 1 GPU in 
the minimum environment. CUDA support. Larger HW configurations with different 
sizing SHALL be required for demanding workloads.  

**Applications:**  Different tools include a mix of development and clinical 
research tools like JupyterLab, OHIF viewer, Python development environment, 
Git, VS Code.  

**Application Version Control:** Developers have permission and MAY install 
different versions of software. These include development tools as well as 
virtualization solutions such as Python virtual environments, containers 
(typically Docker), and virtual machines to isolate different software versions 
from each other to avoid version conflicts.

**Security:** These environments fall under the institutional security
requirements and it SHOULD be the responsibility of the individual developers to
make sure those requirements are being met.  

**Access Control:** Inside institutions, system level access MAY be integrated 
with central IAM (identity and access management) systems. Regardless of how the
user account is provisioned, users SHALL have `sudo` access to the operating 
system.  Users SHALL be responsible for setting access controls that restrict 
application level access from outside of this workstation to software that they 
are developing.

**Integration:**  These systems are typically not integrated with any clinical
systems.  

**Support:**  These systems MAY fall outside of the typical IT support
and not get much support from centralized IT.  

**Availability:** best effort


### Development/Integration Server Environment ###

A single, multi-user system, where developers, data scientists, and clinicians 
are collaborating on experimental software versions and new algorithms. 

**Users:** Developers, data scientists, IT administrators, and clinicians.

**Operating System:**  A native Linux (ex: RedHat, Ubuntu) server environment, where
IT administrators and developers MAY install experimental versions of software.

**Hardware:**  Large workstation, dedicated server or dedicated VM on a shared
system.  CUDA support. Larger HW configurations (GPU, CPU and memory) compared
to the Workstation environment.  

**Applications:**  Several server based applications MAY share the same 
hardware. Applications MAY include a mix of development and clinical research 
tools like JupyterLab, OHIF viewers, Python development environment, MONAI 
Label. Given the scarcity of GPU computing resources available sometimes these 
same development servers MAY be used for both training and deployment workloads.  

**Application Version control:** Less heterogeneous than the workstation 
environment, with typically single main version of the application is available.
These systems MAY run containers (typically Docker), and virtual machines to 
isolate different software versions from each other to avoid version conflicts.  
Applications installed on this environment SHALL NOT have a Kubernetes 
requirement. Each application is managed separately, mostly still by application
developers or experienced IT administrators.  

**Security:** These environments fall under the institutional security 
requirements, managed by IT administrators and SHOULD take care of both, system 
level security as well as application level security.   

**Access Control:** Inside institutions, this system level access is almost always
integrated with central IAM (identity and access management) systems.
Application level access control SHALL be restricted to application developers
for only those users who are authorized.  

**Integration:**  Inside institutions,
these systems MAY be integrated with other research systems, such as research
PACS, DICOM routers, clinical image viewers.  

**Availability:** best effort  


### Staging Server Environment ###

A staging system that mimics production environments with data, type of
integration.  The purpose of this system is for testing and staging purposes,
not for development. Given the early nature of AI development, some institutions
MAY have combined staging and production systems.

**Users:** Developers, data scientists, IT administrators, clinicians.

**Operating System:**  A native Linux (ex: RedHat, Ubuntu) server environment.

**Hardware:**  Large workstation, dedicated server or dedicated VM on a shared
system. CUDA support. Larger HW configurations (GPU, CPU and memory) compared to
the Integration environment.  

**Orchestration:** Kubernetes based container
orchestration.  

**Applications:**  Representative applications to what SHALL run
on the production server.  Applications limited to production and runtime
versions. No development tools.  

**Application Version control:** A single main version of the application is 
available.  Alternative versions of applications MAY be made available. 
Application versions and deployment in this environment SHALL be managed by 
Kubernetes. Applications involved in the end to end workflow are managed by 
experienced IT administrators. 

**Security:** These environments fall under the institutional security 
requirements, managed by IT administrators and SHOULD take care of both, system 
level security as well as application level security.  

**Access Control:** System level access SHALL be restricted access to
only systems or people who have the need to access for testing or maintenance
purposes. Inside institutions, this system level access is almost always
integrated with central IAM (identity and access management) systems.
Application level access control SHALL be restricted to clinicians, application
developers or application administrators for only those users who are
authorized.  

**Integration:**  These systems SHALL be integrated with other
research systems, such as research PACS, DICOM routers, clinical image viewers.

**Availability:** 98% (~a week of unplanned downtime per year)


### Production Server Environment ###

A production system that serves clinical deployment needs, integrated with other
production clinical systems dealing with real patient data.  

**Users:** IT administrators, application administrators, clinicians.

**Operating System:**  A native Linux (ex: RedHat, Ubuntu) server environment.

**Hardware:**  One or more dedicated servers or dedicated VMs on a shared
system, depending on availability and performance requirements. CUDA support.
Larger HW configurations (GPU, CPU and memory) compared to the Staging
environment.

**Applications:**  Production versions of applications, approved
within the institution for clinical deployment.

**Application Version Control:**
One ore more approved versions of each application is available. Application 
versions and deployment in this environment SHALL be managed by Kubernetes.
Applications involved in the end to end workflow are approved by the institution
change control board and managed by experienced IT administrators.

**Security:** These environments fall under the institutional security 
requirements, managed by IT administrators who SHALL take care of both, system 
level security as well as application level security.  

**Access Control:** System level access SHALL be restricted access to only 
systems or people who have the need to access for testing or maintenance 
purposes. Inside institutions, this system level access is almost always 
integrated with central IAM (identity and access management) systems. 
jApplication level access control SHALL be restricted to clinicians or
application administrators for only those users who are authorized.

**Integration:** Inside institutions, these systems SHALL be integrated with
other clinical production systems, such as clinical PACS, DICOM routers,
clinical image viewers.

**Availability:** Highly available, varying from 99%
availability to 99.999%

### Cloud Environments ###

Cloud service providers (Azure, AWS, GCP, ..?) MAY be used as an extension or as
a primary location for one or more of the above environments. 

For workstation and development the primary cloud resource SHALL be a dedicated
Linux VM inside a private network compartment.

For staging and production, the preferred cloud resource SHALL be a managed
Kubernetes service.
