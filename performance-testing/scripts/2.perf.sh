#!/bin/bash
# Copyright 2023 MONAI Consortium
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,  software
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,  either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

CORRELATIONID=$1
NAMESPACE=${2:-default}
MC_ALIAS=argologs
MC_LOGS_BUCKET=argologs
MIG_LOGS=/opt/monai-deploy/mig/logs/MIG*.log
MWM_LOGS=/opt/monai-deploy/mwm/logs/MWM*.log
MTM_LOGS=/opt/monai-deploy/mtm/logs/MWM*.log

print_header() {
    echo "NAME           Start TIme      End Time      Duration"

}
print_time() {
    local name=$1
    local start_time=$2
    local end_time=$3
    local duration=$4
    
    if [ "$start_time" != "N/A" ]; then
        start_time=$(date --date="$start_time" -Ins -u)
    else
        start_time="N/A................................"
    fi 
    if [ "$end_time" != "N/A" ]; then
        end_time=$(date --date="$end_time" -Ins -u)
    else
        end_time="N/A................................"
    fi 

    echo "$name          $start_time     $end_time     $duration"
}

time_diff() {
    local start_time_str=$1
    local end_time_str=$2

    local start_time=$(date --date="$start_time_str" '+%s.%N')
    local end_time=$(date --date="$end_time_str" '+%s.%N')
    local time_diff=$(echo $end_time - $start_time | bc -l)
    echo $time_diff
}
export NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")
export MIG_POD=$(kubectl get po --namespace $NAMESPACE -l app=mig -o jsonpath={..metadata.name})
export MWM_POD=$(kubectl get po --namespace $NAMESPACE -l app=mwm -o jsonpath={..metadata.name})
export MTM_POD=$(kubectl get po --namespace $NAMESPACE -l app=mtm -o jsonpath={..metadata.name})
export ARGO_SERVICE_NAME=$(kubectl get svc --namespace $NAMESPACE -l app.kubernetes.io/name=argo-workflows-server -o jsonpath={..metadata.name})
export ARGO_PORT=$(kubectl get --namespace $NAMESPACE service/$ARGO_SERVICE_NAME -o jsonpath="{.spec.ports[0].port}")
export ARGO_IP=$(kubectl get --namespace $NAMESPACE service/$ARGO_SERVICE_NAME -o jsonpath="{.spec.clusterIP}")
export MINIO_PORT=$(kubectl get --namespace $NAMESPACE service/minio -o jsonpath="{.spec.ports[0].port}")
export MINIO_IP=$(kubectl get --namespace $NAMESPACE service/minio -o jsonpath="{.spec.clusterIP}")

# echo NODE_IP=$NODE_IP
# echo MIG_POD=$MIG_POD
# echo MWM_POD=$MWM_POD
# echo MTM_POD=$MTM_POD
# echo ARGO_SERVICE_NAME=$ARGO_SERVICE_NAME
# echo ARGO_PORT=$ARGO_PORT
# echo ARGO_IP=$ARGO_IP
# echo MINIO_PORT=$MINIO_PORT
# echo MINIO_IP=$MINIO_IP

echo Setting up MinIO client argocli=http://$MINIO_IP:$MINIO_PORT/...
mc alias set $MC_ALIAS http://$MINIO_IP:$MINIO_PORT/ monai minioadmin >/dev/null

echo Scanning logs for CORRELATIONID=${CORRELATIONID}...
# ====== PERF.01 ================================================================
START_TIME=$(grep -h "EventId\": 210" $MIG_LOGS | jq -r "select(.Association | test(\"$CORRELATIONID\")) | .timestamp")
TIME=$(grep -h "EventId\": 214" $MIG_LOGS | jq -r "select(.correlationId==\"$CORRELATIONID\") | .durationSeconds" )
print_time "PERF.01" "$START_TIME" "N/A" "$TIME"

# ====== PERF.02 ================================================================
TIME=$(grep -h "EventId\": 712" $MIG_LOGS | jq -r "select(.CorrelationId==\"$CORRELATIONID\") | .durationSeconds" )
print_time "PERF.02" "N/A" "N/A" "$TIME"

# ====== PERF.03 ================================================================
WORKFLOW_REQUEST_MESSAGEID=$(grep -h "EventId\": 10002" $MWM_LOGS | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\" and .topic==\"md.workflow.request\") | .[\"@messageId\"]" )
TASK_DISPATCH_MESSAGEID=$(grep -h "EventId\": 10000" $MWM_LOGS | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\" and .topic==\"md.tasks.dispatch\") | .[\"@messageId\"]" )
DURATION=$(grep -h "EventId\": 10005" $MWM_LOGS | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\" and .messageId==\"$WORKFLOW_REQUEST_MESSAGEID\") | .durationMilliseconds" )
DURATION_MS=`echo "scale=2;${DURATION}/1000" | bc`
print_time "PERF.03" "N/A" "N/A" "$DURATION_MS"

# ====== PERF.04 ================================================================
DURATION=$(grep -h "EventId\": 10005" $MTM_LOGS | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\" and .[\"@messageId\"]==\"$TASK_DISPATCH_MESSAGEID\") | .durationMilliseconds" )
DURATION_MS=`echo "scale=2;${DURATION}/1000" | bc`
print_time "PERF.04" "N/A" "N/A" "$DURATION_MS"

# ====== PERF.05 ================================================================
TASK_CALLBACK_LOG=$(grep -h "EventId\": 10002" $MTM_LOGS  | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\" and .topic==\"md.tasks.callback\")" )
TASK_CALLBACK_MESSAGE_ID=$(echo $TASK_CALLBACK_LOG | jq -r .[\"@messageId\"])

TIME_START=$(echo $TASK_CALLBACK_LOG | jq -r .timestamp)
TIME_END=$(grep -h "EventId\": 107" $MTM_LOGS  | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\" and .[\"@messageId\"]==\"$TASK_CALLBACK_MESSAGE_ID\") | .timestamp" )
print_time "PERF.05" "$TIME_START" "$TIME_END" $(time_diff "$TIME_START" "$TIME_END")

# ====== PERF.06 ================================================================
TASK_UPDATE_MESSAGEID=$(grep -h "EventId\": 10000" $MTM_LOGS | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\" and .messageType==\"md.tasks.callback\" and .messageId==\"$TASK_CALLBACK_MESSAGE_ID\") | .[\"@messageId\"]")
TIME_START=$(grep -h "EventId\": 10000" $MTM_LOGS | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\" and .messageType==\"md.tasks.callback\" and .messageId==\"$TASK_CALLBACK_MESSAGE_ID\") | .timestamp")
TIME_END=$(grep -h "EventId\": 200016" $MWM_LOGS  | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\" and .[\"@messageId\"]==\"$TASK_UPDATE_MESSAGEID\") | .timestamp")

print_time "PERF.06" "$TIME_START" "$TIME_END" $(time_diff "$TIME_START" "$TIME_END")

ARGO_JOB_NAME=$(grep -h "EventId\": 1008" $MTM_LOGS  | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\") | .name" )
ARGO_JOB_ID=$(curl -s http://$ARGO_IP:$ARGO_PORT/api/v1/archived-workflows | jq -r --arg name "${ARGO_JOB_NAME}" '.items[] | select(.metadata.name == $name) | .metadata.uid')

# ====== PERF.07 ================================================================
TIME_START=$(curl -s http://$ARGO_IP:$ARGO_PORT/api/v1/archived-workflows/${ARGO_JOB_ID} | jq -r .status.startedAt)
TIME_END=$(curl -s http://$ARGO_IP:$ARGO_PORT/api/v1/archived-workflows/${ARGO_JOB_ID} | jq -r .status.finishedAt)
print_time "PERF.07" "$TIME_START" "$TIME_END" $(time_diff "$TIME_START" "$TIME_END")

# ====== PERF.08 ================================================================
TIME_START=$(curl -s http://$ARGO_IP:$ARGO_PORT/api/v1/archived-workflows/${ARGO_JOB_ID} | jq -r '.status.nodes | map(select(.displayName | contains("-step"))) | .[].startedAt')
TIME_END=$(curl -s http://$ARGO_IP:$ARGO_PORT/api/v1/archived-workflows/${ARGO_JOB_ID} | jq -r '.status.nodes | map(select(.displayName | contains("-step"))) | .[].finishedAt')
print_time "PERF.08" "$TIME_START" "$TIME_END" $(time_diff "$TIME_START" "$TIME_END")

# ====== PERF.09 ================================================================
LOG_FILE=$(curl -s http://$ARGO_IP:$ARGO_PORT/api/v1/archived-workflows/${ARGO_JOB_ID} | jq -r '.status.nodes | map(select(.displayName | contains("-step"))) | .[].outputs.artifacts | map (select(.name=="main-logs")) | .[].s3.key')
LOG_CONTENT=$(mc cat $MC_ALIAS/$MC_LOGS_BUCKET/$LOG_FILE)
TIME_START=$(mc cat $MC_ALIAS/$MC_LOGS_BUCKET/$LOG_FILE | head -n 1)
TIME_END=$(mc cat $MC_ALIAS/$MC_LOGS_BUCKET/$LOG_FILE | tail -n 1)
print_time "PERF.09" "$TIME_START" "$TIME_END" $(time_diff "$TIME_START" "$TIME_END")

# ====== PERF.10 ================================================================

TIME_START=$(curl -s http://$ARGO_IP:$ARGO_PORT/api/v1/archived-workflows/${ARGO_JOB_ID} | jq -r '.status.nodes | map(select(.displayName=="send-message")) | .[].startedAt')
TIME_END=$(curl -s http://$ARGO_IP:$ARGO_PORT/api/v1/archived-workflows/${ARGO_JOB_ID} | jq -r '.status.nodes | map(select(.displayName=="send-message")) | .[].finishedAt')
print_time "PERF.10" "$TIME_START" "$TIME_END" $(time_diff "$TIME_START" "$TIME_END")

# ====== PERF.11 ================================================================
TIME_TO_EXPORT=$(grep -h "EventId\": 505" $MIG_LOGS | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\") | .durationMilliseconds")
EXOORT_COMPLETE_TIME=$(grep -h "EventId\": 505" $MIG_LOGS | jq -r "select(.[\"@correlationId\"]==\"$CORRELATIONID\") | .timestamp")

DURATION_MS=`echo "scale=2;${TIME_TO_EXPORT}/1000" | bc`
print_time "PERF.11" "N/A" "$EXOORT_COMPLETE_TIME" "$DURATION_MS"

# ====== PERF.12 ================================================================

print_time "PERF.12" "$START_TIME" "$EXOORT_COMPLETE_TIME" "$(time_diff "$START_TIME" "$EXOORT_COMPLETE_TIME")"



echo ===========================================================================
echo Workflow Request Message ID = ${WORKFLOW_REQUEST_MESSAGEID}
echo Task Dispatch Message ID    = ${TASK_DISPATCH_MESSAGEID}
echo Task Callback Message ID    = ${TASK_CALLBACK_MESSAGE_ID}
echo Task Update Message ID      = ${TASK_UPDATE_MESSAGEID}
echo Argo Job Name               = ${ARGO_JOB_NAME}
echo Argo Job UID                = ${ARGO_JOB_ID}

