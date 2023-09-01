#!/bin/bash
# Copyright 2023 MONAI Consortium
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

echo Waiting for MONAI Deploy service to be ready...
kubectl wait --for=condition=Ready po -l 'app in (mig,mwm,mtm)' >/dev/null
sleep 3
echo ""

export NODE_IP=$(kubectl get nodes --namespace $1 -o jsonpath="{.items[0].status.addresses[0].address}")

export MIG_POD=$(kubectl get po --namespace $1 -l app=mig -o jsonpath={..metadata.name})
export MIG_API_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[1].nodePort}" services mig)
export MIG_DIMSE_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[0].nodePort}" services mig)

export MWM_POD=$(kubectl get po --namespace $1 -l app=mwm -o jsonpath={..metadata.name})
export MWM_API_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[0].nodePort}" services mwm)

export MTM_POD=$(kubectl get po --namespace $1 -l app=mtm -o jsonpath={..metadata.name})
export MTM_API_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[0].nodePort}" services mtm)

ORTHANC_POD=$(kubectl get pod --namespace $1 -l app=orthanc -o jsonpath={..metadata.name})
export ORTHANC_IP=$(kubectl get pod --namespace $1 $ORTHANC_POD -o jsonpath={.status.podIP})
export ORTHANC_API_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[0].nodePort}" services orthanc)
export ORTHANC_DIMSE_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[1].nodePort}" services orthanc)

export MINIO_API_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[0].nodePort}" services minio)
export MINIO_CONSOLE_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[1].nodePort}" services minio)

export RABBITMQ_API_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[0].nodePort}" services rabbitmq)
export RABBITMQ_CONSOLE_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[1].nodePort}" services rabbitmq)

export ARGO_SERVICE_NAME=$(kubectl get svc --namespace $1 -l app.kubernetes.io/name=argo-workflows-server -o jsonpath={..metadata.name})
export ARGO_PORT=$(kubectl get --namespace $1 service/$ARGO_SERVICE_NAME -o jsonpath="{.spec.ports[0].port}")
export ARGO_IP=$(kubectl get --namespace $1 service/$ARGO_SERVICE_NAME -o jsonpath="{.spec.clusterIP}")

export MONGO_PORT=$(kubectl get --namespace $1 -o jsonpath="{.spec.ports[0].nodePort}" services mongo)

echo ====================================
echo Informatics Gateway:
echo - POD:         $MIG_POD
echo - API:         http://$NODE_IP:$MIG_API_PORT
echo - DIMSE Port:  $MIG_DIMSE_PORT
echo - Commands:
echo .   - kubectl describe pod/$MIG_POD
echo .   - kubectl logs -f $MIG_POD
echo ====================================
echo Workflow Manager:
echo - POD:         $MWM_POD
echo - API:         http://$NODE_IP:$MWM_API_PORT
echo - Commands:
echo .   - kubectl describe pod/$MWM_POD
echo .   - kubectl logs -f $MWM_POD
echo ====================================
echo Task Manager:
echo - POD:         $MTM_POD
echo - API:         http://$NODE_IP:$MTM_API_PORT
echo - Commands:
echo .   - kubectl describe pod/$MTM_POD
echo .   - kubectl logs -f $MTM_POD
echo ====================================
echo Orthanc:
echo - POD:         $(kubectl get po --namespace $1 -l app=orthanc -o jsonpath={..metadata.name})
echo - POD IP       $ORTHANC_IP
echo - API:         http://$NODE_IP:$ORTHANC_API_PORT
echo - DIMSE Port:  $ORTHANC_DIMSE_PORT
echo ====================================
echo MinIO:
echo - POD:         $(kubectl get po --namespace $1 -l app=minio -o jsonpath={..metadata.name})
echo - API:         http://$NODE_IP:$MINIO_API_PORT
echo - Console:     http://$NODE_IP:$MINIO_CONSOLE_PORT
echo ====================================
echo RabbitMQ:
echo - POD:         $(kubectl get po --namespace $1 -l app=rabbitmq -o jsonpath={..metadata.name})
echo - API:         http://$NODE_IP:$RABBITMQ_API_PORT
echo - Console:     http://$NODE_IP:$RABBITMQ_CONSOLE_PORT
echo ====================================
echo MongoDB:       
echo - POD:         $(kubectl get po --namespace $1 -l app=mongodb -o jsonpath={..metadata.name})
echo - POrt:         $MONGO_PORT
echo ====================================
echo Argo Workflow:       
echo - POD:         $(kubectl get po --namespace $1 -l app=mongodb -o jsonpath={..metadata.name})
echo - Console:         http://$ARGO_IP:$ARGO_PORT
echo - Commands:
echo .   - kubectl port-forward services/$ARGO_SERVICE_NAME $ARGO_PORT:$ARGO_PORT
echo ====================================


printf "\nDeleting existing MONAI Deploy AE Title..."
curl -s --request DELETE "http://$NODE_IP:$MIG_API_PORT/config/ae/MONAI-DEPLOY" >/dev/null
printf "\nDeleting existing DICOM Source..."
curl -s --request DELETE "http://$NODE_IP:$MIG_API_PORT/config/source/ORTHANC" >/dev/null
printf "\nDeleting existing DICOM Destination..."
curl -s --request DELETE "http://$NODE_IP:$MIG_API_PORT/config/destination/ORTHANC" >/dev/null

printf "\nAdding MONAI Deploy AE Title..."
curl -s --request POST "http://$NODE_IP:$MIG_API_PORT/config/ae" --header "Content-Type: application/json" --data-raw "{\"name\": \"MONAI-DEPLOY\",\"aeTitle\": \"MONAI-DEPLOY\"}" >/dev/null
printf "\nAdding DICOM Source..."
curl -s --request POST "http://$NODE_IP:$MIG_API_PORT/config/source" --header "Content-Type: application/json" --data-raw "{\"name\": \"ORTHANC\",\"hostIp\": \"$ORTHANC_IP\",\"aeTitle\": \"ORTHANC\"}" >/dev/null
printf "\nAdding DICOM Destination..."
curl -s --request POST "http://$NODE_IP:$MIG_API_PORT/config/destination" --header "Content-Type: application/json" --data-raw "{\"name\": \"ORTHANC\",\"hostIp\": \"$NODE_IP\",\"port\": $ORTHANC_DIMSE_PORT,\"aeTitle\": \"ORTHANC\"}" >/dev/null

printf "\nMONAI Deploy AE Titles:\n"
curl -f --request GET "http://$NODE_IP:$MIG_API_PORT/config/ae" 2>/dev/null | jq
printf "\nDICOM Sources:\n"
curl -f --request GET "http://$NODE_IP:$MIG_API_PORT/config/source" 2>/dev/null | jq
printf "\nDICOM Destinations:\n"
curl -f --request GET "http://$NODE_IP:$MIG_API_PORT/config/destination" 2>/dev/null | jq
