# Description #
Solution is a basic .net webapp for sending DICOMs and Rabbit messages. This will be used during performance testing by hitting the relevant endpoints to generate traffic to MIG and MWM via Rabbit. This will allow components to be tested in isolation or as a complete E2E process.

# Getting Started #
## Dependencies ##
- .net 6
- Docker
- MWM and its dependencies
- MIG and its dependencies
- Dummy models (to be included as part of MWM development)

## Running Tests ##
### MONAI Informatics Gateway ###
You will need to:

- Deploy MIG to a suitable environment including all of its dependencies (Minio, RabbitMQ, ELK).
- Configure dotnet-performance-app to point to the MIG.
- Configure k6 app to specify relevant load profile.
- Perform GET requests on the dicom/{modality} endpoints.
- Review logs in logging DB for time metrics.

### MONAI Workflow Manager ###
You will need to:

- Deploy MWM to a suitable environment including all of its dependencies (Mongo, RabbitMQ, ELK, dummy models).
- Configure dotnet-performance-app to point to the event message broker deployed.
- Seed Mongo with Workflow Revisions
- Configure k6 app to specify relevant load profile.
- Perform GET requests on the rabbit/{workflow} endpoints.
- Review logs in logging DB for time metrics.

### MIG and MWM ###
You will need to:

- Deploy MIG to a suitable environment including all of its dependencies (Minio, RabbitMQ, ELK).
- Deploy the MWM to a suitable environment including all of its dependencies (Mongo, RabbitMQ, ELK, dummy models).
- Configure dotnet-performance-app to point to the event message broker deployed.
- Seed Mongo with Workflow Revisions
- Configure k6 app to specify relevant load profile.
- Perform GET requests on the dicom/{modality} endpoints.
- Review logs in logging DB for time metrics.

---

## Running locally ##

## Prerequisites ##

* .net 6.0
* [K6](https://k6.io/docs/getting-started/installation/)
* Docker & docker-compose

## Installation ##

* Clone the repo
* Run `dotnet build` in the terminal

## Start Docker services ##

* Run `docker-compose up -d`

## Start the server ##

* Run `dotnet run`

## Start the performance tests ##

### RabbitMQ ###

* Run `k6 run -e CONFIG=config/{appropriate-config-file} tests/rabbit.js`

### Dicom ###

* Run `k6 run -e CONFIG=config/{appropriate-config-file} tests/dicom.js`