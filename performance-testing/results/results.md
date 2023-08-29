# Introduction #
This report documents the baseline and load tests against the AIDE. It shows comparisons of baseline and load tests across an AWS cloud environment (SIT) and performant on-premise Pre Prod environment. It also lists any conclusions and identifies any necessary follow-up actions.

# Environment Details #

## AWS Cloud (SIT) Specification ##

| Node      | Specification              |
|-----------|----------------------------|
| SIT-Head1 | 4 vCPU, 16GB ram, 0 GPUs   |
| SIT-Head2 | 4 vCPU, 16GB ram, 0 GPUs   |
| SIT-DGX   | 8 vCPUs, 32GB ram, 1 GPU's |

## On-premise Pre Prod Environment ## 

| Node      | Specification              |
|-----------|----------------------------|
| PreProd-Head1 | 48 vCPU, 252GB ram, 1 GPUs   |
| PreProd-Head2 | 48 vCPU, 252GB ram, 0 GPUs   |
| PreProd-Head3   | 48 vCPUs, 252GB ram, 1 GPU's |


# Data #
| Modality | Details                   |
| -------- | ------------------------- |
| RF       | \- 1 slice<br>\- 1MB      |
| US       | \- 7 slices<br>\- 17MB    |
| MR       | \- 5 slices<br>\- 1MB     |
| CT       | \- 324 slices<br>\- 167MB |

# Applications #
The following dummy applications were published to stress the GPU and CPU. These were written using [stress](https://linux.die.net/man/1/stress) and [gpu-burn](https://github.com/wilicc/gpu-burn)

| Application Name | Specification                                                            | Modality  |
| ---------------- | ------------------------------------------------------------------------ | --------- |
| Small            | CPU: 2<br>GPU: Access to all<br>RAM: 1GB<br>Execution time: 10 seconds   | RF        |
| Medium           | CPU: 8<br>GPU: Access to all<br>RAM: 10GB<br>Execution time: 30 seconds  | US and MR |
| Large            | CPU: 12<br>GPU: Access to all<br>RAM: 16GB<br>Execution time: 60 seconds | CT        |

# Test Types #

## Baseline ##
Single transactions to performance reference point which can be used as a basis for performance comparison

## Load Average ##
Realistic expected usage levels to determine its response time, resource usage, and reliability using GSTT imaging throughput data in an average 1 hour period.

## Load Peak ##
Realistic expected usage levels to determine its response time, resource usage, and reliability using GSTT imaging throughput data in an peak 1 hour period.

## Stress ##
Uplift of peak load by 25% 

# Throughput #

## Peak 1 Hour ##

| Modality   | Transactions | Model executions |
| ---------- | ------------ | ---------------- |
| X-ray      | 120          | 120              |
| Ultrasound | 50           | 5                |
| CT         | 30           | 21               |
| MRI        | 25           | 17.5             |

## Avg 1 Hour ##

| Modality   | Transactions | Model executions |
| ---------- | ------------ | ---------------- |
| X-ray      | 60          | 60              |
| Ultrasound | 28           | 2.8                |
| CT         | 10           | 7               |
| MRI        | 13           | 9.1             |

## Stress 1 Hour ##

| Modality   | Transactions | Model executions |
| ---------- | ------------ | ---------------- |
| X-ray      | 180          | 180              |
| Ultrasound | 75           | 7.5                |
| CT         | 45           | 31.5               |
| MRI        | 37.5           | 26.25             |


# KPI and Measurements #

| KPI                     | Details                                                                                                                                                  | Query Params                                                                                                          |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| DICOM Payload Processed | How long it took between an association being made to Informatics Gateway, the instances being saved to MinIO and a WorkflowRequestEvent being generated | ServiceName: Monai.Deploy.InformaticsGateway AND "Payload took"                                                       |
| Task Dispatched         | How long it took for the WorkflowRequestEvent to be consumed by the WorkflowManager, a workflow to be triggered and a TaskDispatchEvent to be generated  | ServiceName: Monai.Deploy.WorkflowManager AND messageDescription: WorkflowRequestEvent AND durationMilliseconds > 0   |
| Task Created            | How long it took for the TaskDispatchEvent to be consumed by the TaskManager and create a Task                                                           | ServiceName: Monai.Deploy.WorkflowManager.TaskManager AND messageType: TaskDispatchEvent AND durationMilliseconds > 0 |
| Task Update             | How long it took for the TaskManager to publish a TaskUpdateEvent, the WorkflowManager to consume the event and update the WorkflowInstance              | ServiceName: Monai.Deploy.WorkflowManager AND messageDescription: TaskUpdateEvent AND durationMilliseconds > 0        |
| Argo                    | How long it took for Argo to run the application requested. This includes time from the pod being scheduled and then a TaskCallbackEvent being published | Taken from Argo                                                                                                       |
| End To End              | Indicative time of the end to end processing of a workflow from dicom association to workflow completion.                                                | Time from Task Update timestamp - (DICOM Payload Process timestamp - processed time)                                  |

# Cloud Execution #

## Details ##
Baseline tests were executed on SIT to validate the cloud environment to compare pre-prod tests against to understand the performance improvements based on specifications.

## Results ##
### Baseline ###
#### Description ####
Send through the same study 5 times, with a 90 second gap to get average metric for a known study, environment and MAP (liver-seg) set up.

#### Metrics ####
|          | DICOM Payload Processed | DICOM Payload Processed | Task Dispatched | Task Dispatched | Task Created  | Task Created | Task Update   | Argo      | Argo          | Argo      | End to End |
| -------- | ----------------------- | ----------------------- | --------------- | --------------- | ------------- | ------------ | ------------- | --------- | ------------- | --------- | ---------- |
| Modality | Average            | Max               | Average    | Max       | Average  | Max     | Average  | Max  | Average (min) | Max (min) | Indicative |
| CT       | 01:11                   | 01:24                   | 14.5            | 20.4            | 2.3           | 2.9          | 0.8           | 1.7       | 01:57         | 02:04     | 03:21      |
| MR       | 13.6                    | 34.5                    | 6.7             | 13.6            | 4.9           | 10           | 1             | 1.5       | 01:24         | 01:32     | 01:23      |
| US       | 6.2                     | 6.8                     | 2.6             | 3.3             | 2.8           | 3.9          | 0.7           | 1.5       | 01:14         | 01:15     | 01:25      |
| RF       | 5.8                     | 9.5                     | 11.3            | 23.6            | 30            | 107.7        | 1.1           | 2.9       | 01:06         | 01:37     | 00:58      |

# On-Premise Execution #

## Details ##
Baseline, Load and Stress tests were executed on on-premise to understand the performance of MONAI-Deploy and AIDE on target production hardware and validate against throughput and metrics.

## Results ##
### Baseline 1 ###
#### Description ####
Send through the same study 5 times, with a 90 second gap to get average metric for a known study, environment and MAP (liver-seg) set up.

#### Metrics ####
|                                                              | DICOM Payload Processed | DICOM Payload Processed | Task Dispatched | Task Dispatched | Task Created  | Task Created | Task Update   | Task Update | Argo          | Argo      | End to End |
| ------------------------------------------------------------ | ----------------------- | ----------------------- | --------------- | --------------- | ------------- | ------------ | ------------- | ----------- | ------------- | --------- | ---------- |
| Modality                                                     | Average (sec)           | Max (sec)               | Average (sec)   | Max (sec)       | Average (sec) | Max (sec)    | Average (sec) | Max (sec)   | Average (min) | Max (min) | Indicative |
| CT ("{{ context.dicom.series.all('0008','0060') }} == 'CT'") | 34.4                    | 36.2                    | 11.6            | 12.5            | 1.1           | 1.2          | 0.4           | 0.9         | 01:54         | 02:07     | 02:30      |
| CT ("{{ context.dicom.series.any('0008','0060') }} == 'CT'") | 34.2                    | 37.8                    | 12.3            | 13.7            | 1.2           | 1.6          | 0.7           | 1           | 01:53         | 02:03     | N/A        |
| MR                                                           | 1.1                     | 1.4                     | 0.7             | 1.1             | 1.2           | 1.5          | 0.6           | 0.8         | 01:06         | 01:10     | 01:18      |
| US                                                           | 1.7                     | 2.3                     | 1.1             | 1.3             | 0.9           | 1.6          | 0.6           | 1           | 01:10         | 01:17     | 01:07      |
| RF                                                           | 0.7                     | 1.2                     | 0.7             | 1.1             | 0.9           | 1.3          | 0.8           | 1           | 00:55         | 00:58     | 00:42      |
| CT (executing Small app & no conditional logic)              | 34.9                    | 37.9                    | 10.6            | 10.8            | 2.08          | 6.3          | 0.9           | 1.9         | 01:06         | 01:13     | 01:47      |
| RF (no conditional logic)                                    | 0.7                     | 0.9                     | 0.8             | 1.4             | 1.3           | 1.8          | 0.7           | 1.3         | 00:55         | 01:00     | 00:52      |

### Baseline 2 ###
#### Description ####
Retest of the MIG following a change to how it was saving data to MinIO.

|          | DICOM Payload Processed | DICOM Payload Processed |
| -------- | ----------------------- | ----------------------- |
| Modality | Average (sec)           | Max (sec)               |
| CT       | 14                      | 16.2                    |

### Load (Avg) ###
#### Description ####
#### Metrics ####

### Load (Peak) ###
#### Description ####
#### Metrics ####

### Stress ###
#### Description ####
#### Metrics ####
