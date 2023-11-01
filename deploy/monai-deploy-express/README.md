# MONAI Deploy Express

**This is NOT recommended for production environments**

As described in the [MONAI Operating Environments guideline](https://github.com/Project-MONAI/monai-deploy/blob/main/guidelines/MONAI-Operating-Environments.md), the journey from development to production usually requires multiple steps across different environments, operated by different teams and with different requirements.

MONAI Deploy Express is designed to facilitate the testing and validation of MAPs in the early stages of this pipeline (i.e. workstation environment), where ease of use and time to get started are most important.

Users of MONAI Deploy Express will be able to run their MAPs, connected to a test PACS, or their own test/research PACS, for further validation, confidently taking steps towards production.   

Reusing the same essential core services for DICOM I/O and AI workflow orchestration provides the same functionality and consistent experience independently of where and how the applications are run, with minimal changes for the end user.


## Prerequisites

### Ubuntu 20.04 or later

- [Docker Engine](https://docs.docker.com/engine/install/) v20.10.18+
- [Docker Compose Plug-in](https://docs.docker.com/compose/install/) v2.10.2+
- [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) v11.7+
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- MONAI Deploy MAPs built using the [MONAI Deploy App SDK](https://github.com/Project-MONAI/monai-deploy-app-sdk)
- [curl](https://curl.se/) - `sudo apt install curl`
- (Optional) [Informatics Gateway CLI](https://github.com/Project-MONAI/monai-deploy-informatics-gateway/releases)

### Windows Subsystem for Linux v2

- [WSLv2](https://docs.microsoft.com/en-us/windows/wsl/install)
- [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)
  - With `Use the WSL 2 based engine` option enabled
  - Make sure that the [Nvidia Container Runtime](https://github.com/Project-MONAI/monai-deploy/tree/main/deploy/monai-deploy-express#enable-nvidia-container-runtime-for-docker) is enabled
- [Ubuntu 22.04](https://www.microsoft.com/store/productId/9PN20MSR04DW) for WSL 2
- [NVIDIA Windows Driver](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) for WSL 2
- [curl](https://curl.se/) - `sudo apt install curl`
- (Optional) [Informatics Gateway CLI](https://github.com/Project-MONAI/monai-deploy-informatics-gateway/releases)


**IMPORTANT: Please ensure all prerequisites are up-to-date.**

*Note: see the [tips](#tips) section for additional instructions.*

## Installation

To use MONAI Deploy Express, install all prerequisites & download this entire directory from [GitHub](https://github.com/Project-MONAI/monai-deploy/tree/main/deploy/monai-deploy-express) or from the [release page](https://github.com/Project-MONAI/monai-deploy/releases).
You can also deploy MONAI Deploy Express automatically on AWS Cloud by using the automation package located in the [platforms/AWS directory](https://github.com/Project-MONAI/monai-deploy/tree/main/deploy/monai-deploy-express/platforms/AWS) of this GitHub repository.

## Start/Stop the Services

The [Docker compose file](docker-compose.yml) spins up the following services. Services are accessible at the IP addresses and ports listed below and may be modified in the [.env](.env) configuration file.

Execute one of the following commands in the directory where the `docker-compose.yml` resides to start, stop all the services or to view the logs.

```bash
docker compose up # start MONAI Deploy Express
docker compose up -d # or run detached
docker compose logs -t -f # view output from all containers
docker compose down # stop all services
```

Use the following commands to launch MONAI Deploy Express with ELK (ElasticSearch-LogStash-Kibana):

```bash
./init.sh # required to setup Elastic volume mapping permissions on Linux
docker compose --profile elk up # start MONAI Deploy Express & ELK
docker compose --profile elk up -d # or run detached
docker compose logs -t -f # view output from all containers
docker compose --profile elk down # stop all services
```

The first time calling `docker compose up` may take longer as it needs to pull all the container images. However, once all container images are pulled and available on the local system, all the services should spin up between 20 to 65 seconds.

### MONAI Deploy Services

| Service                 | Host IP/Port          | Internal IP/Port        |
| ----------------------- | --------------------- | ----------------------- |
| Informatics Gateway UI  | http://localhost:5000 | http://172.29.0.50:5000 |
| Informatics Gateway SCP | 104                   | 104                     |
| Workflow Manager        | http://localhost:5001 | http://172.29.0.60:5001 |
| Task Manager            | N/A                   | N/A                     |

### Third-Party Services

| Service                                                         | Host IP/Port           | Internal IP/Port         |
| --------------------------------------------------------------- | ---------------------- | ------------------------ |
| MinIO (default storage service)                                 | http://localhost:9001  | http://172.29.0.10:9001  |
| RabbitMQ (default message broker service)                       | http://localhost:15672 | http://172.29.0.20:15672 |
| MongoDB (default database for Worklflow Manager & Task Manager) | http://localhost:27017 | http://172.29.0.30:27017 |
| Orthanc UI (optional)                                           | http://localhost:8042  | http://172.29.0.100:8042 |
| Orthanc SCP (optional)                                          | 4242                   | 4242                     |
| Elastic Search                                                  | 9200, 9300             | 9200,9300                |
| Log Stash                                                       | 9600, 50000            | 9600, 50000              |
| Kibana                                                          | http://localhost:5601  | http://172.29.0.103:5601 |

*Note: Orthanc is included for convenience and to demo end-to-end workflow execution. It may be disabled and have MONAI Deploy Express integrated with external Orthanc, PACS or other DICOM devices.*

*Note: The `172.29.0.0/16` subnet is for container communication. If the subnet is not available, please refer to the [Advanced Configuration](#advanced-configuration) on how to update the subnet.*

### Common/Known Issues

- The following error indicates that the `docker compose` version may not be up-to-date. If the problem persists, modify the `TASK_MANAGER_DATA` variable defined in the `.env` file and change `$PWD/.md/mdtm` to a fully qualified path. E.g. `/home/monai/some/path/to/.md/mdtm/`.
    ```
    ERROR: Named volume "$PWD/.md/mdtm:/var/lib/mde:rw" is used in service "task-manager" but no declaration was found in the volumes section. 
    ```

    *WHY? The value of `TASK_MANAGER_DATA` is exposed to the Task Manager container as an environment variable in order for Task Manager to map the volume from the host to the MAP container correctly.*

- The Informatics Gateway service is unhealthy and fails to start with the following error if Docker is not up-to-date:
  ```bash
  > docker logs mdl-ig
  Failed to create CoreCLR, HRESULT: 0x80070008
  ```
  
  - If you start Monai Deploy Express from within a container, you are likely to have problems when starting the system with 'docker compose up', such as:
    ```
    ERROR: Named volume "$PWD/.md/mdtm:/var/lib/mde:rw" is used in service "task-manager" but no declaration was found in the volumes section. 
    ```
   
- If you start Monai Deploy Express from within a container, you are likely to have problems when starting the system with 'docker compose up', such as:
  ```
  Error response from daemon: failed to create shim: runc create failed: unable to start container process: error during init: 
  error mounting "/workspace/monai-deploy-express/configs/informatics-gateway.json:/opt/monai/ig.appsettings.json" 
  (via /proc/self/fd/6), flags: 0x5000: not a directory: unknown: are you trying to mount a directory onto a file (or vice-versa)?
  ```
  _CAUSE - Docker Compose has some problems resolving files and directories, which only seem to happen inside a container. When launching the hosting container, if you mount a volume to the original host directory using the same path internally, this should work e.g._
  ```
  -v /home/myuser/monai-deploy-express:/home/myuser/monai-deploy-express
  ```
## Running a MONAI Deploy Workflow

This package includes Orthanc running and connected to the Informatics Gateway, with all required AE Titles pre-configured.

To get started, download & unzip the following DICOM datasets and upload them to Orthanc.

- [Chest CT dataset](https://drive.google.com/file/d/1IGXUgZ7NQCwsix57cdSgr-iYErevqETO/view?usp=sharing)
- [Abdomen CT dataset](https://drive.google.com/file/d/1d8Scm3q-kHTqr_-KfnXH0rPnCgKld2Iy/view?usp=sharing)

Note: these DICOM datasets were converted to DICOM from Medical Decathlon training and validation images and may be used for the referenced examples later in this document.

### Upload DICOM Datasets

Navigate to Orthanc via http://localhost:8042, and click *Upload* on the top right-hand corner.
Drag & drop any DICOM files (no folders) to the blue box on the page and then click *Start the upload*.

Or, upload your files to Orthanc using the *storescu* command from [dcmtk](https://dcmtk.org/dcmtk.php.en).
```
storescu -v +r +sd -aec ORTHANC localhost 4242 /path/to/my/unzipped/dicom/files/*
```

Navigate to the home page and click *All studies* to confirm data's been uploaded.

## Sample Workflows

The **sample-workflows** directory includes the following four sample workflow definitions:

- `hello-world.json `: Hello World!
- `lung-seg.json`: AI Lung Segmentation MAP
- `liver-seg.json`: AI Liver Segmentation MAP
- `liver-lung-seg.json`: AI Lung & AI Liver Combo
- `liver-tumor.json`: AI Liver Tumor 2.0 MAP (MONAI Deploy 0.6)

*Note: in these examples, we will be using `curl` command to register MONAI Deploy workflow definitions with the Workflow Manager. To learn more about `curl`, visit the [curl Man Page](https://curl.se/docs/manpage.html).*

### Hello World

#### Description

This example uses the `alpine` container image instead of a MAP to print all files found in the input directory; this example demonstrates how data received by the Informatics Gateway travel through MONAI Deploy and how the data is made available to the application container.

#### Steps

1. Deploy the workflow definition to MONAI Deploy Workflow Manager:
   ```
   curl --request POST --header 'Content-Type: application/json'  --data "@sample-workflows/hello-world.json"  http://localhost:5001/workflows
   ```
   Output:
   ```
   {"workflow_id":"849d4683-006b-410c-aa17-d0474ee26b7b"}
   ```
   If the `curl` command runs successfully, expect a `workflow_id` to be returned and printed to the terminal.
2. Navigate to Orthanc, select any study and then click *Send to DICOM Modality* from the menu on the left.
   In the popup dialog, select **MONAI-DEPLOY** to start a C-STORE request to the Informatics Gateway.
3. To see the output from the container, run the following commands:
   ```bash
   > docker container list -a | grep alpine
   # locate the container ID and run the following
   > docker logs {CONTAINER ID}
   # expect a list of files to be printed
   /var/monai/input/1.2.826.0.1.3680043.2.1125.1.19616861412188316212577695277886020/1.2.826.0.1.3680043.2.1125.1.34918616334750294149839565085991567/1.2.826.0.1.3680043.2.1125.1.60545822758941849948931508930806372.dcm.json
   /var/monai/input/1.2.826.0.1.3680043.2.1125.1.19616861412188316212577695277886020/1.2.826.0.1.3680043.2.1125.1.34918616334750294149839565085991567/1.2.826.0.1.3680043.2.1125.1.60545822758941849948931508930806372.dcm
   ...
   ```

### AI Liver Segmentation MAP

#### Description

In this section, we will download a DICOM dataset, upload it to Orthanc and then run the [Liver Segmentation MAP](https://github.com/Project-MONAI/monai-deploy-app-sdk/tree/0.5.1/examples/apps/ai_livertumor_seg_app) from the
[MONAI Deploy App SDK](https://github.com/Project-MONAI/monai-deploy-app-sdk). Finally, we can expect the AI-generated segmentation result to appear in Orthanc.


#### Steps

1. Download the [Abdomen CT dataset](#running-a-monai-deploy-workflow) dataset
2. Download the AI Liver Tumor MAP
   ```bash
   docker pull ghcr.io/mmelqin/monai_ai_livertumor_seg_app:1.0
   ```
3. Upload the dataset as described in [Uploading Data](#upload-dicom-datasets)
4. Deploy the workflow definition to MONAI Deploy Workflow Manager:
5. 
   ```bash
   curl --request POST --header 'Content-Type: application/json'  --data "@sample-workflows/liver-seg.json"  http://localhost:5001/workflows
   ```

   If the `curl` command runs successfully, expect a `workflow_id` to be returned and printed to the terminal:

   ```
   {"workflow_id":"811620da-381f-4daa-854d-600948e67228"}
   ```
   
6. Navigate to Orthanc, select any study and then click *Send to DICOM Modality* from the menu on the left.
   In the popup dialog, select **MONAI-DEPLOY** to start a C-STORE request to the Informatics Gateway.
7. Wait for the workflow to complete; the entire workflow takes roughly one minute and thirty seconds to complete. To see the AI-generated segmentation object, reload the Orthanc study page.
8. To see the output of the container, run the following commands:
   ```bash
   > docker container list -a | grep monai_ai_livertumor_seg_app
   # locate the container ID and run the following
   > docker logs {CONTAINER ID}
   ```

### AI Lung Segmentation MAP

#### Description

In this section, we will download a DICOM dataset, upload it to Orthanc and then run the **Lung Segmentation MAP** from the
[MONAI Deploy App SDK](https://github.com/Project-MONAI/monai-deploy-app-sdk). Finally, we can expect the AI-generated segmentation result to appear in Orthanc.

#### Steps

1. Download the [Chest CT dataset](#running-a-monai-deploy-workflow) dataset
2. Download the AI Lung Segmentation MAP
   ```bash
   docker pull ghcr.io/mmelqin/monai_ai_lung_seg_app:1.0
   ```
3. Upload the dataset as described in [Uploading Data](#upload-dicom-datasets)
4. Deploy the workflow definition to MONAI Deploy Workflow Manager:
5. 
   ```
   curl --request POST --header 'Content-Type: application/json'  --data "@sample-workflows/lung-seg.json"  http://localhost:5001/workflows
   ```

   If the `curl` command runs successfully, expect a `workflow_id` to be returned and printed to the terminal:

   ```
   {"workflow_id":"811620da-381f-4daa-854d-600948e67228"}
   ```

6. Navigate to Orthanc, select any study and then click *Send to DICOM Modality* from the menu on the left.
   In the popup dialog, select **MONAI-DEPLOY** to start a C-STORE request to the Informatics Gateway.
7. Wait for the workflow to complete; the entire workflow takes roughly one minute to complete. To see the AI-generated segmentation object, reload the Orthanc study page.
8. To see the output from the container, run the following commands:
   ```bash
   > docker container list -a | grep monai_ai_lung_seg_app
   # locate the container ID and run the following
   > docker logs {CONTAINER ID}
   ```

### AI Lung + AI Liver MAPs

In the `liver-lung-seg.json` workflow definition, we combined the AI Lung MAP and the AI Liver MAP into one single workflow definition. With this workflow definition, the Workflow Manager would route the incoming data based on the routing rules defined.

   1. Download one or both of the [datasets](#running-a-monai-deploy-workflow) provided above
   2. Download the AI Liver Tumor & the AI Lung Segmentation MAPs
      ```bash
      docker pull ghcr.io/mmelqin/monai_ai_lung_seg_app:1.0
      docker pull ghcr.io/mmelqin/monai_ai_livertumor_seg_app:1.0
      ```
   3. Upload the dataset as described in [Uploading Data](#upload-dicom-datasets)
   4. Deploy the workflow definition to MONAI Deploy Workflow Manager:
   5. 
      ```
      curl --request POST --header 'Content-Type: application/json'  --data "@sample-workflows/liver-lung-seg.json"  http://localhost:5001/workflows
      ```

      If the `curl` command runs successfully, expect a `workflow_id` to be returned and printed to the terminal:

      ```
      {"workflow_id":"6d5e1e73-bd07-4e71-b1fa-b66408d43b82"}
      ```

   6. Navigate to Orthanc, select one of the studies and then click *Send to DICOM Modality* from the menu on the left.
      In the popup dialog, choose **MONAI-DEPLOY** to start a C-STORE request to the Informatics Gateway.
   7. Wait for the workflow to complete and reload the Orthanc study page and expect a new series to be added.
   8. To see the output from the container, run the following commands:
      ```bash
      > docker container list -a | grep monai_ai_
      # locate the container ID and run the following
      > docker logs {CONTAINER ID}
      ```
   9. Repeat the steps with the other dataset.

In this example, the [Chest CT dataset](https://drive.google.com/file/d/1IGXUgZ7NQCwsix57cdSgr-iYErevqETO/view?usp=sharing) should only launch the AI Lung MAP, while the [Abdomen CT dataset](https://drive.google.com/file/d/1d8Scm3q-kHTqr_-KfnXH0rPnCgKld2Iy/view?usp=sharing) would launch the AI Liver MAP.

### AI Liver Tumor 2.0 MAP

#### Description

In this section, we will download a DICOM dataset, upload it to Orthanc and then run the [Liver Segmentation MAP](https://github.com/Project-MONAI/monai-deploy-app-sdk/tree/0.6.0/examples/apps/ai_livertumor_seg_app) from the
[MONAI Deploy App SDK](https://github.com/Project-MONAI/monai-deploy-app-sdk). Finally, we can expect the AI-generated segmentation result to appear in Orthanc.


#### Steps

1. Download the [Abdomen CT dataset](#running-a-monai-deploy-workflow) dataset
2. Download the AI Liver Tumor 2.0 MAP
   ```bash
   docker pull ghcr.io/mmelqin/monai_ai_livertumor_seg_app_stl-x64-workstation-dgpu-linux-amd64:2.0
   ```
3. Upload the dataset as described in [Uploading Data](#upload-dicom-datasets)
4. Deploy the workflow definition to MONAI Deploy Workflow Manager:
5. 
   ```bash
   curl --request POST --header 'Content-Type: application/json'  --data "@sample-workflows/liver-tumor.json"  http://localhost:5001/workflows
   ```

   If the `curl` command runs successfully, expect a `workflow_id` to be returned and printed to the terminal:

   ```
   {"workflow_id":"811620da-381f-4daa-854d-600948e67228"}
   ```
   
6. Navigate to Orthanc, select any study and then click *Send to DICOM Modality* from the menu on the left.
   In the popup dialog, select **MONAI-DEPLOY** to start a C-STORE request to the Informatics Gateway.
7. Wait for the workflow to complete; the entire workflow takes roughly one minute and thirty seconds to complete. To see the AI-generated segmentation object, reload the Orthanc study page.
8. To see the output of the container, run the following commands:
   ```bash
   > docker container list -a | grep monai_ai_livertumor_seg_app_stl
   # locate the container ID and run the following
   > docker logs {CONTAINER ID}
   ```


## Using Kibana

A default dataview is imported to Kibana at startup. To load the saved search, navigate to http://localhost:5601/, click on Analytics > Discover from the 🍔 menu. From the top right click *Open* and select *MONAI-Default*.


## Tips

- If you are using your DICOM dataset, please remove the router task or modify the routing conditions to meet your needs.
- If all four sample workflow definitions are registered, and one of the provided DICOM studies is sent, then three workflows are executed. For example, the Chest CT dataset would trigger three workflows: `Hello World`, `AI Lung MAP`, and the `AI Lung + Liver MAP`.
- If your system is running low on storage space, look into `.md/` directory. With the default configuration (in `.dev`), data uploaded to Orthanc can be found in `.md/orthanc/`. Data sent for workflow processing can be found in `.md/minio/`.
- MONAI Deploy Express includes MinIO as the default storage service and RabbitMQ as the default message broker service. To use different service providers, refer to these [instructions](./plug-ins/README.md).
- Changes to the AE Titles, IPs, or port numbers require deleting the `.md/mdig/` directory.
- The `configs/config-ig.sh` script configures the listening AE Title and configures Orthanc as a DICOM source & DICOM destination.  Avoid using `ORTHANC` as the name of the source & destination as the script resets them to the bundled Orthanc setup.


### Enable NVIDIA Container Runtime for Docker

To enable NVIDIA runtime for Docker, append the following section to `/etc/docker/daemon.json` for Linux. For WSLv2, open Docker Desktop Settings and go to Docker Engine and append the following:

```json
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
```

### WSL

If you encounter an error in section 3 on [CUDA Support for WSL 2](https://docs.nvidia.com/cuda/wsl-user-guide/index.html#cuda-support-for-wsl2), use the following:

```bash
 sudo apt-key del 7fa2af80

 wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
 sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
 wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda-repo-wsl-ubuntu-11-7-local_11.7.0-1_amd64.deb
 sudo dpkg -i cuda-repo-wsl-ubuntu-11-7-local_11.7.0-1_amd64.deb

 sudo cp /var/cuda-repo-wsl-ubuntu-11-7-local/*.gpg /usr/share/keyrings/

 sudo apt-get update
 sudo apt-get -y install cuda
```

## Advanced Configuration

### Docker-Compose Configuration

All services included in the `docker-compose` file may be customized through the default environment file, `.env`, file.

All services run in the `172.29.0.0/16` subnet, and the values can be found in the `.env` file.

*Note: Changing any IP address or port number requires an update to the applicable service configuration files.*

- Informatics Gateway: [informatics-gateway.json](configs/informatics-gateway.json)
- Workflow Manager: [workflow-manager.json](configs/workflow-manager.json)
- Task Manager: [task-manager.json](configs/task-manager.json)
- Orthanc: [orthanc.json](configs/orthanc.json)

### Configure External DICOM Devices/PACS

To accept DICOM dataset from external DICOM devices or PACS, first, configure your external PACS to register MONAI Deploy as a data destination:

- Port: 104 (see `INFORMATICS_GATEWAY_SCP_PORT` in `.env` file)
- AE Title: MONAI-DEPLOY (see `INFORMATICS_GATEWAY_AE_TITLE` in `.env` file)

Informatics Gateway is configured in this package to accept any association from any DICOM devices. To disable this feature and enable data source validation, set `rejectUnknownSources` to `true` in the [informatics-gateway.json](configs/informatics-gateway.json). Once `rejectUnknownSources` is set to `true`, you must register each data source using `curl`. Check out [config-ig.sh](configs/config-ig.sh) for examples and [Configuration API](https://monai.io/monai-deploy-informatics-gateway/api/rest/config.html#post-configsource) for the complete reference.

To export DICOM results to external DICOM devices, you must first register them with the Informatics Gateway using `curl`. Check out [config-ig.sh](configs/config-ig.sh) for examples and [Configuration API](https://monai.io/monai-deploy-informatics-gateway/api/rest/config.html#post-configdestination) for the complete reference.

Any changes made in this section must also reflect in your workflow definition. Therefore, follow the next section to compose your workflow definition.

### Composing a Workflow

A MONAI Deploy [workflow definition](https://github.com/Project-MONAI/monai-deploy-workflow-manager/blob/77c4ef2212ecf3917ddfdcd743f08aa160c5fd6c/guidelines/mwm-workflow-spec.md) is what drives your clinical AI workflows and is fully customizable. In this section, we will explain the fields defined in the `liver-seg.json` example.

*Note: IG is an abbreviation of the Informatics Gateway.*

```json
{
    "name": "ai-liver-seg", # name of the workflow
    "version": "1.0.0", # version of the workflow
    "description": "AI Liver Segmentation", # a description of the workflow
    "informatics_gateway": { # defines data ingestion and export
        "ae_title": "MONAI-DEPLOY", # name of the IG AE Title receiving your DICOM data
        "data_origins": [ # one or more external DICOM devices sending data to the IG
            "ORTHANC" # Name of that external DICOM device (name configured in IG)
        ],
        "export_destinations": [ # zero or more external DICOM devices that will be receiving AI-generated results
            "ORTHANC" # Name of that external DICOM device (name configured in IG)
        ]
    },
    "tasks": [ # one or more tasks allowed
        {
            "id": "router", # name of the task
            "description": "Ensure series description contains liver", # description of the task
            "type": "router", # router denotes we are routing data to another task or tasks based on the conditions
            "task_destinations": [ # list of downstream tasks to be executed when this task completes
                {
                    "name": "liver", # if the following condition matches, the dataset is routed to the liver task.
                    "conditions": "{{ context.dicom.series.any('0008','103E')}} == 'CT series for liver tumor from nii 014'" # matches series description by the value specified.
                }
            ]
        },
        {
            "id": "liver", # name of the task
            "description": "Execute Liver Segmentation MAP", # description of the task
            "type": "docker", # docker denotes we are running this task using Docker plug-in
            "args": {
                "container_image": "ghcr.io/mmelqin/monai_ai_livertumor_seg_app:1.0", # container image
                "server_url": "unix:///var/run/docker.sock", # how the Docker plug-in communicates with Docker API
                "entrypoint": "/bin/bash,-c", # entrypoint of your container image; separated by commas
                "command": "python3 -u /opt/monai/app/app.py", # commands to execute with the container image; separated by commas
                "task_timeout_minutes": "5", # how long this task is expected to execute; terminated after the configured value
                "temp_storage_container_path": "/var/lib/mde/", # how thd Docker plug-in maps your data from host to container - this is mapped to `$TASK_MANAGER_DATA` in the docker-compose file 
                "env_MONAI_INPUTPATH": "/var/monai/input/", # an environment varible provided to the container to read the input data
                "env_MONAI_OUTPUTPATH": "/var/monai/output/", # an environment variable provided to the container to write AI-genrated results
                "env_MONAI_MODELPATH": "/opt/monai/models/", # an environment variable provided to the container to located AI models
                "env_MONAI_WORKDIR": "/var/monai/" # an environment variable provided to the container for storing temporary artifacts
            },
            "artifacts": {
                "input": [ # one or more input artifacts/volumes mapped to the container
                    {
                        "name": "env_MONAI_INPUTPATH", # name of the input where your application is reading input data from; must be defined in the args section with a valid path internal to the container
                        "value": "{{ context.input.dicom }}" # the container expects DICOM data
                    }
                ],
                "output": [# zero or more output artifacts/volumes mapped to the container
                    {
                        "name": "env_MONAI_OUTPUTPATH", # name of the output where your application is writing final results to; msut be defined in the args section with a valid path internal to the container
                        "mandatory": true
                    }
                ]
            },
            "task_destinations": [ # list of downstream tasks to be executed when this task completes
                {
                    "name": "export-liver-seg" # name of the downstream task
                }
            ]
        },
        {
            "id": "export-liver-seg", # name of the task
            "description": "Export Segmentation Storage Object", # description of the task
            "type": "export", # export denotes that we are exporting data
            "export_destinations": [ # one or more export destinations where the results from the output of the previous task would be exported to
                {
                    "Name": "ORTHANC" # name of the export destination as defined in the informatics_gateway>export_destinations section above
                }
            ],
            "artifacts": {
                "input": [ # one or more data input that included the files to be exported
                    {
                        "name": "export-dicom", # name of the input
                        "value": "{{ context.executions.liver.artifacts.env_MONAI_OUTPUTPATH }}", # an expression used to located the source of the data. In this case, the Workflow Manager would locate the data from the task named `liver` with an output artifact named `env_MONAI_OUTPUTPATH`
                        "mandatory": true # true if we must export the result; if the results can't be located, the workflow would be considered as failed; false otherwise.
                    }
                ],
                "output": []
            }
        }
    ]
}
```



## Uninstallation

- Stop all services (run inside the directory where docker-compose.yml resides)
  
  ```bash
  docker compose down 
  ```

- Delete MONAI Deploy Docker images
  
  ```bash
  docker rmi $(docker images | grep 'monai-deploy')
  ```

- Delete this package & data directories. By default, all data are stored under the `.md` directory where the `docker-compose.yml` file is stored.
  
  ```bash
  sudo rm -r DIR_TO_THE_PACKAGE
  ```


## Links

- [MONAI Deploy](https://github.com/Project-MONAI/monai-deploy) 
  - [Issues](https://github.com/Project-MONAI/monai-deploy/issues)
  - [Discussions](https://github.com/Project-MONAI/monai-deploy/discussions)
- [MONAI Deploy App SDK](https://github.com/Project-MONAI/monai-deploy-app-sdk)
  - [Issues](https://github.com/Project-MONAI/monai-deploy-app-sdk/issues)
  - [User Guide](https://docs.monai.io/projects/monai-deploy-app-sdk/en/latest/introduction/index.html)
- [MONAI Deploy Informatics Gateway](https://github.com/Project-MONAI/monai-deploy-informatics-gateway) 
  - [Issues](https://github.com/Project-MONAI/monai-deploy-informatics-gateway/issues)
  - [User Guide](https://monai.io/monai-deploy-informatics-gateway/)
- [MONAI Deploy Workflow Manager & Task Manager](https://github.com/Project-MONAI/monai-deploy-workflow-manager)
  - [Issues](https://github.com/Project-MONAI/monai-deploy-workflow-manager/issues)
- [MONAI Deploy Storage Library](https://github.com/Project-MONAI/monai-deploy-storage)
- [MONAI Deploy Messaging Library](https://github.com/Project-MONAI/monai-deploy-messaging/)

## License

Copyright (c) MONAI Consortium. All rights reserved. Licensed under the Apache-2.0 license.

Refer to the license page of each service/component linked in the above section for additional information.
