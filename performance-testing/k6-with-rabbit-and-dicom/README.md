# k6-with-rabbit-and-dicom

This is a set of performance tests for RabbitMQ and PACS using K6 and an express app to facilitate the connection between K6 and Rabbit/PACS.

## Prerequisites

* Node
* Javascript
* [K6](https://k6.io/docs/getting-started/installation/)
* Docker & docker-compose

## Installation

* Clone the repo
* Run `npm install` in the terminal

## Start Docker services

* Run `docker-compose up -d`

## Start the server

* Run `npm start`

## Start the performance tests

### RabbitMQ

* Run `k6 run tests/rabbit.js`

### Dicom

* Run `k6 run -e CONFIG=config/{appropriate-config-file} tests/dicom.js`
