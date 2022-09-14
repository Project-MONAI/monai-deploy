# MONAI Deploy Lite

MONAI Deploy Lite provides a simple & lightweight solution for running MONAI Applications (MAPs) on a minimal MONAI Deploy platform.

It is meant to bridge the big gap between the local development of MAPs in a laptop using the MONAI Deploy App SDK and a production-ready deployment. 

Users of MONAI Deploy Lite will be able to run their MAPs, connected to a test PACS, or their own test/research PACS, for further validation, confidently taking steps towards production.   

Reusing the same essential core services for DICOM I/O and AI workflow orchestration provides the same functionality and consistent experience independently of where and how the applications are run, with minimal changes for the end user.


## Prerequisites

- [Docker Engine](https://docs.docker.com/engine/install/) v20.10.18+
- [Docker Compose Plug-in](https://docs.docker.com/compose/install/) v2.10.2+
- MONAI Deploy MAPs built using the [MONAI Deploy App SDK](https://github.com/Project-MONAI/monai-deploy-app-sdk)
- [jq](https://stedolan.github.io/jq/)
- (Optional) [Informatics Gateway CLI](https://github.com/Project-MONAI/monai-deploy-informatics-gateway/releases)

## Installation

To use MONAI Deploy Lite, install all prerequisites & download this entire directory from [GitHub](https://github.com/Project-MONAI/monai-deploy/tree/main/docker-compose/deploy/docker-compos). 

## Start the Services

The [docker compose file](docker-compose.yml) spins up the following services. Each service may be accessed at the IP and port described below using the default [.env](.env) configuration file.

Execute the following command to bring up all services.

```bash
docker compose up
docker compose up -d # or run detached
docker compose logs -t -f # view output from all containers
```

### MONAI Deploy Services
- Informatics Gateway - http://localhost:5000 or http://172.29.0.50:5000
  - SCP Port 104
- Workflow Manager - http://localhost:5001 or http://172.29.0.60:5001
- Task Manager - http://localhost:5002 or http://172.29.0.70:5002

### Third-Party Services
- MinIO (default storage service) - http://localhost:9001 or http://172.29.0.10:9001
- RabbitMQ (default message broker service) - http://localhost:15672 or http://172.29.0.20:15672
- MongoDB (default database for Worklfow Manager & Task Manager) - http://localhost:27017 or http://172.29.0.30:27017
- Orthanc (optional) - http://localhost:8042 or http://172.29.0.100:8042
  - SCP Port 4242

Note: Orthanc service is included for convenience to demo end-to-end workflow execution. It may be disabled and have MONAI Deploy Lite integrated with external Orthanc, PACS or other DICOM devices,

## Running a MONAI Deploy Workflow

This package includes Orthanc running and connected to the Informatics Gateway, with all required AE Titles pre-configured.

To get started, upload any DICOM dataset to Orthanc. If you don't have any DICOM dataset available, please feel free to download the [Chest CT dataset](https://drive.google.com/file/d/1IGXUgZ7NQCwsix57cdSgr-iYErevqETO/view?usp=sharing) or [Abdomen CT dataset](https://drive.google.com/file/d/1d8Scm3q-kHTqr_-KfnXH0rPnCgKld2Iy/view?usp=sharing). These datasets were converted to DICOM from Medical Decathlon training and validation mages & may be used for the referenced examples later in this document.

### Uploading Data

Navigate to Orthanc via http://localhost:8042 or http://172.29.0.100:8042, and click *Upload* on the top right-hand corner.
Drag & drop any DICOM files (no folders) to the blue box on the page and then click *Start the upload*.

Or, upload your files to Orthanc using the *storescu* command from [dcmtk](https://dcmtk.org/dcmtk.php.en).
```
storescu -v +r +sd -aec ORTHANC localhost 4242 /path/to/my/dicom/*
```

Navigate to the home page and click *All studies* to confirm data's been uploaded.

## Sample Workflows

Under the **sample-workflows* directory, a couple of sample workflow definitions are provided:

- `hello-world.json `: Hello World!
- `lung-seg.json`: AI Lung Segmentation MAP
- `liver-seg.json`: AI Liver Segmentation MAP
- `combo.json`: Workflow with both AI Lung & AI Liver MAPs

### Hello World

#### Description

This example uses the `alpine` image to print all files found in the input directory simply.

1. Deploy the workflow definition to MONAI Deploy Workflow Manager:
   ```
   $ curl --request POST --header 'Content-Type: application/json'  --data "@sample-workflows/hello-world.json"  http://localhost:5001/workflows

   {"workflow_id":"849d4683-006b-410c-aa17-d0474ee26b7b"}
   ```
   If the `curl` command runs successfully, expect a `workflow_id` to be returned and printed to the terminal.
1. Navigate to Orthanc, select any study and then click *Send to DICOM Modality* from the menu on the left.
   In the popup dialog, select **MONAI-DEPLOY** to start a C-STORE request to the Informatics Gateway.
1. To see the output from the container, run the following commands:
   ```bash
   $ docker container list -a | grep alpine
   # locate the container ID and run the following
   $ docker logs {CONTAINER ID}
   # expect a list of files to be printed
   /var/monai/input/1.2.826.0.1.3680043.2.1125.1.19616861412188316212577695277886020/1.2.826.0.1.3680043.2.1125.1.34918616334750294149839565085991567/1.2.826.0.1.3680043.2.1125.1.60545822758941849948931508930806372.dcm.json
   /var/monai/input/1.2.826.0.1.3680043.2.1125.1.19616861412188316212577695277886020/1.2.826.0.1.3680043.2.1125.1.34918616334750294149839565085991567/1.2.826.0.1.3680043.2.1125.1.60545822758941849948931508930806372.dcm
   ...
   ```

### AI Liver Segmentation MAP

#### Description

In this section, we will download a DICOM dataset, upload it to Orthanc and then run the [Liver Segmentation MAP](https://github.com/Project-MONAI/monai-deploy-app-sdk/tree/main/examples/apps/ai_livertumor_seg_app) from the
[MONAI Deploy App SDK](https://github.com/Project-MONAI/monai-deploy-app-sdk). Finally, we can expect the AI-generated segmentation result to appear in Orthanc.

1. Download the dataset from [here](https://drive.google.com/file/d/1d8Scm3q-kHTqr_-KfnXH0rPnCgKld2Iy/view?usp=sharing)
2. Upload the dataset as described in [Uploading Data](#uploading-data)
3. Deploy the workflow definition to MONAI Deploy Workflow Manager:
   ```
   $ curl --request POST --header 'Content-Type: application/json'  --data "@sample-workflows/liver-seg.json"  http://localhost:5001/workflows

   {"workflow_id":"811620da-381f-4daa-854d-600948e67228"}
   ```
   If the `curl` command runs successfully, expect a `workflow_id` to be returned and printed to the terminal.
4. Navigate to Orthanc, select any study and then click *Send to DICOM Modality* from the menu on the left.
   In the popup dialog, select **MONAI-DEPLOY** to start a C-STORE request to the Informatics Gateway.
5. Wait for the workflow to complete and reload the Orthanc study page and expect a new series to be added.
6. To see the output from the container, run the following commands:
   ```bash
   $ docker container list -a | grep monai_ai_livertumor_seg_app
   # locate the container ID and run the following
   $ docker logs {CONTAINER ID}
   ```

### AI Lung Segmentation MAP

#### Description

In this section, we will download a DICOM dataset, upload it to Orthanc and then run the **Lung Segmentation MAP** from the
[MONAI Deploy App SDK](https://github.com/Project-MONAI/monai-deploy-app-sdk). Finally, we can expect the AI-generated segmentation result to appear in Orthanc.

1. Download the data set from [here](https://drive.google.com/file/d/1IGXUgZ7NQCwsix57cdSgr-iYErevqETO/view?usp=sharing)
2. Upload the dataset as described in [Uploading Data](#uploading-data)
3. Deploy the workflow definition to MONAI Deploy Workflow Manager:
   ```
   $ curl --request POST --header 'Content-Type: application/json'  --data "@sample-workflows/lung-seg.json"  http://localhost:5001/workflows

   {"workflow_id":"811620da-381f-4daa-854d-600948e67228"}
   ```
   If the `curl` command runs successfully, expect a `workflow_id` to be returned and printed to the terminal.
4. Navigate to Orthanc, select any study and then click *Send to DICOM Modality* from the menu on the left.
   In the popup dialog, select **MONAI-DEPLOY** to start a C-STORE request to the Informatics Gateway.
5. Wait for the workflow to complete and reload the Orthanc study page and expect a new series to be added.
6. To see the output from the container, run the following commands:
   ```bash
   $ docker container list -a | grep monai_ai_lung_seg_app
   # locate the container ID and run the following
   $ docker logs {CONTAINER ID}
   ```

### Combo - AI Lung + AI Liver MAPs

In the `combo.json` workflow definition, we combined the AI Lung MAP and the AI Liver MAP into one single workflow definition. With this workflow definition, the Workflow Manager would route the incoming data based on the routing rules defined.

1. Download the data sets from [here](https://drive.google.com/file/d/1d8Scm3q-kHTqr_-KfnXH0rPnCgKld2Iy/view?usp=sharing) and [here](https://drive.google.com/file/d/1IGXUgZ7NQCwsix57cdSgr-iYErevqETO/view?usp=sharing).
2. Upload the dataset as described in [Uploading Data](#uploading-data)
3. Deploy the workflow definition to MONAI Deploy Workflow Manager:
   ```
   $ curl --request POST --header 'Content-Type: application/json'  --data "@sample-workflows/combo.json"  http://localhost:5001/workflows

   {"workflow_id":"6d5e1e73-bd07-4e71-b1fa-b66408d43b82"}
   ```
   If the `curl` command runs successfully, expect a `workflow_id` to be returned and printed to the terminal.
4. Navigate to Orthanc, select one of the studies and then click *Send to DICOM Modality* from the menu on the left.
   In the popup dialog, choose **MONAI-DEPLOY** to start a C-STORE request to the Informatics Gateway.
5. Wait for the workflow to complete and reload the Orthanc study page and expect a new series to be added.
6. To see the output from the container, run the following commands:
   ```bash
   $ docker container list -a | grep monai_ai_lung_seg_app
   # locate the container ID and run the following
   $ docker logs {CONTAINER ID}
   ```

In this example, the [Chest CT dataset](https://drive.google.com/file/d/1IGXUgZ7NQCwsix57cdSgr-iYErevqETO/view?usp=sharing) should only launch the AI Lung MAP, while the [Abdomen CT dataset](https://drive.google.com/file/d/1d8Scm3q-kHTqr_-KfnXH0rPnCgKld2Iy/view?usp=sharing) would launch the AI Liver MAP.

## Tips & Hints

- If you are using your DICOM dataset, please ensure to remove the router task or modify the routing conditions.
- If all four workflow definitions are registered, and only one of the provided DICOM studies was sent, then three workflows are executed. For example, if the Chest CT dataset was sent, then Workflow Manager would launch three workflows: `Hello World`, `AI Lung MAP`, and the `Combo`.

## Advanced Configuration

### Docker-Compose Configuration

All services included in the `docker-compose` file may be customized through the default environment file, `.env`, file 

*Note: Changing any IP address or port number requires an update to the applicable service configuration files.*

- Informatics Gateway: [informatics-gateway.json](configs/informatics-gateway.json)
- Workflow Manager: [workflow-manager.json](configs/workflow-manager.json)
- Task Manager: [task-manager.json](configs/task-manager.json)
- Orthanc: [orthanc.json](configs/orthanc.json)

### Configure External DICOM Devices/PACS

To accept DICOM dataset from external DICOM devices or PACS, first, configure your external PACS to register MONAI Deploy as a data destination:

- Port: 104 (see `INFORMATICS_GATEWAY_SCP_PORT` in `.env` file)
- AE Title: MONAI-DEPLOY (see `INFORMATICS_GATEWAY_AE_TITLE` in `.env` file)

Informatics Gateway is configured in this package to accept any association from any DICOM devices. To disable this feature and allow data source validation, set `rejectUnknownSources` to `true` in the [informatics-gateway.json](configs/informatics-gateway.json). Once `rejectUnknownSources` is set to `true`, you must register each data source using `curl`. Check out [config-ig.sh](configs/config-ig.sh)) for examples and [Configuration API](https://monai.io/monai-deploy-informatics-gateway/api/rest/config.html#post-configsource) for complete reference.

To export DICOM results to external DICOM devices, you must first register them with the Informatics Gateway using `curl`. Check out [config-ig.sh](configs/config-ig.sh)) for examples and [Configuration API](https://monai.io/monai-deploy-informatics-gateway/api/rest/config.html#post-configdestination) for complete reference.

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
				"temp_storage_container_path": "/var/lib/monai/", # how thd Docker plug-in maps your data from host to container - this is mapped to `$TASK_MANAGER_DATA` in the docker-compose file 
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

- Delete MONAI Deploy Docker images
  ```bash
  docker rmi $(docker images | grep 'monai-deploy')
  ```
- Delete this package & data directories. By default, all data are stored under the `.md` directory where the `docker-compose.yml` file is stored.
  ```bash
  sudo rm -r DIR_TO_THE_PACKAGE

  ```