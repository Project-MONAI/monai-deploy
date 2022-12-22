# Table of Contents
1. [Overview](#overview)
2. [Examples](#examples)
3. [External Links](#faqs)

# Overview
Clinical Workflows are key in defining how inbound data triggers Applications and what happens with the application outputs. A Clinical Workflow is built up of one or more of the following Tasks types, to read the full specification please [here](https://github.com/Project-MONAI/monai-deploy-workflow-manager/blob/develop/docs/setup/mwm-workflow-spec.md)

| Type | Purpose |
| ---- | ------- |
| Argo | A task which will trigger the execution of an Argo Workflow |
| Router | A task to control the flow through a workflow |
| Export | A task to trigger the exporting of data |
| Clinical Review | A task which will allow clinicians to review a previous task |

# Examples
The below examples are indicative only, the details of the tasks may change based on the AET, Applications, Conditions, Artifacts and Exports required.

## Argo Task Example
### Description
Clinical Workflow with an Argo Task.

### Visual
![link](../static/Clinical_Workflows-Argo%20Workflow.drawio.png)

### Clinical Workflow
``` json
{
  "name": "clinical_workflow",
  "version": "1.0.0",
  "description": "Clinical Workflow Example",
  "informatics_gateway": {
    "ae_title": "MONAI",
    "data_origins": [],
    "export_destinations": []
  },
  "tasks": [
    {
      "id": "Application_1",
      "description": "AI Application 1",
      "type": "argo",
      "args": {
        "namespace": "argo",
        "workflow_template_name": "argo-workflow-1",
        "server_url": "https://argo-server.argo:2746",
        "allow_insecure": "true"
      },
      "task_destinations": [],
      "export_destinations": [],
      "artifacts": {
        "input": [
          {
            "name": "input-dicom",
            "value": "{{ context.input.dicom }}",
            "mandatory": true
          }
        ],
        "output": [
          {
            "name": "report-dicom",
            "value": "",
            "mandatory": true
          }
        ]
      },
      "timeout_minutes": -1
    }
  ]
}
```

## Argo Task with Export Example
### Description
Clinical Workflow with an Argo Task with the output being exported to PACS.

### Visual
![link](../static/Clinical_Workflows-Export%20Task.drawio.png)

### Clinical Workflow
``` json
{
  "name": "clinical_workflow",
  "version": "1.0.0",
  "description": "Clinical Workflow Example",
  "informatics_gateway": {
    "ae_title": "MONAI",
    "data_origins": [],
    "export_destinations": [
      "PACS"
    ]
  },
  "tasks": [
    {
      "id": "Application_1",
      "description": "AI Application 1",
      "type": "argo",
      "args": {
        "namespace": "argo",
        "workflow_template_name": "argo-workflow-1",
        "server_url": "https://argo-server.argo:2746",
        "allow_insecure": "true"
      },
      "task_destinations": [
        {
          "name": "Export_Report",
          "conditions": []
        }
      ],
      "export_destinations": [],
      "artifacts": {
        "input": [
          {
            "name": "input-dicom",
            "value": "{{ context.input.dicom }}",
            "mandatory": true
          }
        ],
        "output": [
          {
            "name": "report-dicom",
            "value": "",
            "mandatory": true
          }
        ]
      },
      "timeout_minutes": -1
    },
    {
      "id": "Export_Report",
      "description": "Export Application 1 Report",
      "type": "export",
      "args": {},
      "task_destinations": [],
      "export_destinations": [
        {
          "name": "PACS"
        }
      ],
      "artifacts": {
        "input": [
          {
            "name": "report-dicom",
            "value": "{{ context.executions.Application_1.artifacts.report-dicom }}",
            "mandatory": true
          }
        ],
        "output": []
      },
      "timeout_minutes": -1
    }
  ]
}
```

## Router Task with Conditions 1 Example
### Description
Clinical Workflow with a Router Task which chains onto an Argo task based on modality.

### Visual
![link](../static/Clinical_Workflows-Router%20Task%20with%20conditions.drawio.png)

### Clinical Workflow
``` json
{
  "name": "clinical_workflow",
  "version": "1.0.0",
  "description": "Clinical Workflow Example",
  "informatics_gateway": {
    "ae_title": "MONAI",
    "data_origins": [],
    "export_destinations": []
  },
  "tasks": [
    {
      "id": "router-task",
      "description": "router task to route MR and US studies",
      "type": "router",
      "args": {},
      "task_destinations": [
        {
          "name": "Application_CT",
          "conditions": [
            "{{ context.dicom.series.all('0008','0060') }} == 'CT'"
          ]
        },
        {
          "name": "Application_US",
          "conditions": [
            "{{ context.dicom.series.all('0008','0060') }} == 'US'"
          ]
        }
      ],
      "export_destinations": [],
      "artifacts": {
        "input": [],
        "output": []
      },
      "timeout_minutes": -1
    },
    {
      "id": "Application_CT",
      "description": "CT AI Application",
      "type": "argo",
      "args": {
        "namespace": "argo",
        "workflow_template_name": "argo-workflow-CT",
        "server_url": "https://argo-server.argo:2746",
        "allow_insecure": "true"
      },
      "task_destinations": [],
      "export_destinations": [],
      "artifacts": {
        "input": [
          {
            "name": "input-dicom",
            "value": "{{ context.input.dicom }}",
            "mandatory": true
          }
        ],
        "output": [
          {
            "name": "report-dicom",
            "value": "",
            "mandatory": true
          }
        ]
      },
      "timeout_minutes": -1
    },
    {
      "id": "Application_US",
      "description": "US AI Application",
      "type": "argo",
      "args": {
        "namespace": "argo",
        "workflow_template_name": "argo-workflow-US",
        "server_url": "https://argo-server.argo:2746",
        "allow_insecure": "true"
      },
      "task_destinations": [],
      "export_destinations": [],
      "artifacts": {
        "input": [
          {
            "name": "input-dicom",
            "value": "{{ context.input.dicom }}",
            "mandatory": true
          }
        ],
        "output": [
          {
            "name": "report-dicom",
            "value": "",
            "mandatory": true
          }
        ]
      },
      "timeout_minutes": -1
    }
  ]
}
```

## Router Task with Conditions 2 Example
### Description
Clinical Workflow with a Router Task which chains onto multiple Argo tasks in parallel based on modality.

### Visual
![link](../static/Clinical_Workflows-Router%20Task%20Parallel.drawio.png)

### Clinical Workflow
``` json
{
  "name": "clinical_workflow",
  "version": "1.0.0",
  "description": "Clinical Workflow Example",
  "informatics_gateway": {
    "ae_title": "MONAI",
    "data_origins": [],
    "export_destinations": []
  },
  "tasks": [
    {
      "id": "router-task",
      "description": "router task to route MR and US studies",
      "type": "router",
      "args": {},
      "task_destinations": [
        {
          "name": "Application_CT_1",
          "conditions": [
            "{{ context.dicom.series.all('0008','0060') }} == 'CT'"
          ]
        },
        {
          "name": "Application_CT_2",
          "conditions": [
            "{{ context.dicom.series.all('0008','0060') }} == 'CT'"
          ]
        }
      ],
      "export_destinations": [],
      "artifacts": {
        "input": [],
        "output": []
      },
      "timeout_minutes": -1
    },
    {
      "id": "Application_CT_1",
      "description": "CT AI Application 1",
      "type": "argo",
      "args": {
        "namespace": "argo",
        "workflow_template_name": "argo-workflow-CT-1",
        "server_url": "https://argo-server.argo:2746",
        "allow_insecure": "true"
      },
      "task_destinations": [],
      "export_destinations": [],
      "artifacts": {
        "input": [
          {
            "name": "input-dicom",
            "value": "{{ context.input.dicom }}",
            "mandatory": true
          }
        ],
        "output": [
          {
            "name": "report-dicom",
            "value": "",
            "mandatory": true
          }
        ]
      },
      "timeout_minutes": -1
    },
    {
      "id": "Application_CT_2",
      "description": "CT AI Application 2",
      "type": "argo",
      "args": {
        "namespace": "argo",
        "workflow_template_name": "argo-workflow-CT-2",
        "server_url": "https://argo-server.argo:2746",
        "allow_insecure": "true"
      },
      "task_destinations": [],
      "export_destinations": [],
      "artifacts": {
        "input": [
          {
            "name": "input-dicom",
            "value": "{{ context.input.dicom }}",
            "mandatory": true
          }
        ],
        "output": [
          {
            "name": "report-dicom",
            "value": "",
            "mandatory": true
          }
        ]
      },
      "timeout_minutes": -1
    }
  ]
}
```