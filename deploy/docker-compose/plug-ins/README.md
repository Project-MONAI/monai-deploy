# MONAI Deploy Plug-Ins


## Storage Service Provider

MinIO is included as the default storage service provider. To replace MinIO with your plug-in, refer to the development guide found on https://github.com/Project-MONAI/monai-deploy-storage/.


## Message Broker Service Provider

RabbitMQ is the default messaging provider; to replace RabbitMQ with your plug-in, refer to the development guide found on https://github.com/Project-MONAI/monai-deploy-messaging/.


## Installation

To use your storage or message broker service providers, install the DLLs in this directory.