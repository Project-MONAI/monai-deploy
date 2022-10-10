# Description #
Performance tests have been written to simulate real life load on the MONAI deploy solution stack. This includes benchmark, average and peak load (soak) configuration. Because of the asynchronous architecture of MONAI Deploy, k6 will be used as the load generator but logs from elastic will be used to measure the performance of the individual components.

# Getting Started #
## Dependencies ##
- MWM and its dependencies
- MIG and its dependencies
- Docker
- Orthanc
- Dummy models (to be included as part of MWM development)
- ELK Stack
- Prometheus and Grafana
- Test data (CT, MR, US, RF)

## Architecture ##
- k6
    - Load generator written in Go and can be executed via Docker.
    - Scripting is done in JS or TS.
    - Configuration of load throughput are held in config files [here](./k6/dicom/config/)
    - Will send HTTP STORE requests to Orthanc for a given modality.
- k6 Scripts
    - dicom_benchmark.js - Sends MR study store requests with a 2 minute sleep between each iteration.
    - dicom_peak_avg.js - Sends CT, MR, US and RF study store requests based on the configuration
- Orthanc
    - is an open-source lightweight DICOM server.
    - Will perform C-STORE requests to MIG.
    - 2 modalities set up (MONAI, NOTMONAI) which will send C-STORE with an AET which will either trigger or workflow or wont depending on the Clinical Workflows set up.
- ELK Stack
    - A log aggregator (i.e ELK) will be used for capturing all logs so that investigation of run time metrics can be achieved.
- Grafana and Prometheus
    - Monitoring and visualization platforms to monitor memory, CPU and GPU usage from the applications
- Models
    - Dummy models created will simulate real model usage to stress the system.

![link](./k6/static/Perf%20Architecture.png)

| Name   | CPU Cores | RAM  | GPU  | Disk Space |
| ------ | --------- | ---- | ---- | ---------- |
| Small  | 2         | 1GB  | 1GB  | 2GB        |
| Medium | 8         | 10GB | 6GB  | 15GB       |
| Large  | 12        | 16GB | 12GB | 25GB       |

### Clinical Workflow Example ##
```
AET: MONAI
Tasks [
    {
        name: router
        type: router
        task-destinations{
            if CT run ct-argo
            if MR run mr-argo
            if US run us-argo
            if RF run rf-argo
        }
    },
    {
        name: ct-argo
        type: argo
        args{
            argo-template: large-model
        }
    },
    {
        name: mr-argo
        type: argo
        args{
            argo-template: medium-model
        }
    },
    {
        name: us-argo
        type: argo
        args{
            argo-template: medium-model
        }
    }
    {
        name: rf-argo
        type: argo
        args{
            argo-template: small-model
        }
    }
]
```

## Tests ##
### Baseline/ Benchmark ###
Baseline/ Benchmark tests will be used to measuring the best performance of the MONAI stack. Is this a low throughput test which put no stress on the system. These stats will be used to measure any degradation.

| Modality | Iterations | Typical Image Size | \# of Images / Study | Size (Raw) |
| -------- | ---------- | ------------------ | -------------------- | ---------- |
| MRI      | 10         | (256, 256, 30, 1)  | 200                  | 26mb       |

#### Set Up ####
- Deploy MIG and MWM to an envrironment including all its dependencies.
- Set up MIG with AET and Destinations scripts found [here](TBD)
- Seed Orthanc with Test Data from [here](TBD)
- Set up Orthanc with a Remote Modality, configuration can be found [here](https://book.orthanc-server.com/users/configuration.html#configuration)
    - MONAI - This will be send C-STORE requests to MIG with an AET "MONAI"
- Seed MongoDB with Clinical Workflows found [here](TBD)
- Seed Argo with the Argo Workflow Templates found [here](TBD)
- Install k6 from [here](https://k6.io/docs/getting-started/installation/)
- Update Orthanc details (i.e url) in the config/benchmarkConfig.json

#### Running Tests ####
```bash
cd k6
```

```bash
k6 run -e CONFIG=config/benchmarkConfig.json dicom/dicom_benchmark.js --insecure-skip-tls-verify
```

#### Investigating Metrics ####
##### MONAI Informatics Gateway #####
- Informatics gateway will output logs detailing the time when an association was made and when a WorkflowRequest was sent. This can be seen by | grep "Payload took" which will give a hh:mm:ss between the 2 events.
- Export request times can be seen by checking the time the export request was send and the time an export

##### MONAI Workflow Manager #####
- Logs TBC

##### MONAI Task Manager #####
- Logs TBC

##### Argo #####
- Grafana will be used for visualization of the hardware resources.

### Average and Peak Load ###
Average and Peak load times are displayed as below. These tests are most valuable running on production like hardware to measure performance metrics including processing times as well as system metrics such as CPU, Memory and GPU usage.

| Modality                    | Peak 1 hour      | Avg 1 hour (8-5) | Typical Image Size | \# of Images / Study | Size (Raw) |
| --------------------------- | ---------------- | ---------------- | ------------------ | -------------------- | ---------- |
| X-ray                       | 120              | 60               | (2000, 2500, 1, 1) | 3                    | 30mb       |
| Ultrasound                  | 50               | 28               | (640, 480, 1, 1)   | 30                   | 9.2mb      |
| CT                          | 30               | 10               | (512, 512, 1, 1)   | 60                   | 32mb       |
| Multi Slice CT              | split with above | split with above | (512, 512, 200, 1) | 500                  | 262mb      |
| MRI                         | 25               | 13               | (256, 256, 30, 1)  | 200                  | 26mb       |
| ALL (Inc. other modalities) | 250              | 140              | \-                 | \-                   | \-         |

#### Set Up ####
- Deploy MIG and MWM to an envrironment including all its dependencies.
- Set up MIG with AET and Destinations scripts found [here](TBD)
- Seed Orthanc with Test Data from [here](TBD)
- Set up Orthanc with 2 Remote Modalities, configuration can be found [here](https://book.orthanc-server.com/users/configuration.html#configuration)
    - MONAI - This will be send C-STORE requests to MIG with an AET "MONAI"
    - NOTMONAI - This will be send C-STORE requests to MIG with an AET "NOTMONAI"
- Seed MongoDB with Clinical Workflows found [here](TBD)
- Seed Argo with the Argo Workflow Templates found [here](TBD)
- Install k6 from [here](https://k6.io/docs/getting-started/installation/)
- Update Orthanc details (i.e url) in the config/benchmarkConfig.json

#### Running Tests ####
```bash
cd k6
```
```bash
k6 run -e CONFIG=config/{config}.json dicom/dicom_peak_avg.js --insecure-skip-tls-verify
```

#### Investigating Metrics ####
##### MONAI Informatics Gateway #####
- Informatics gateway will output logs detailing the time when an association was made and when a WorkflowRequest was sent. This can be seen by | grep "Payload took" which will give a hh:mm:ss between the 2 events.
- Export request times can be seen by checking the time the export request was send and the time an export

##### MONAI Workflow Manager #####
- Logs TBC

##### MONAI Task Manager #####
- Logs TBC

##### Argo #####
- Grafana will be used for visualization of the hardware resources.
