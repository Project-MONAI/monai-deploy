#!/bin/bash
# Copyright 2022 MONAI Consortium
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

echo "===Configuring Informatics Gateway==="
echo "Informatics Gateway IP Address = $1"
echo "Informatics Gateway Port       = $2"
echo "Informatics Gateway AE TItle   = $3"
echo "Orthanc IP Address             = $4"
echo "Orthanc SCP Port               = $5"
echo -e "\n"

printf "\nDeleting existing MONAI Deploy AE Title\n"
curl --request DELETE "http://$1:$2/config/ae/MONAI-DEPLOY" | jq
printf "\nDeleting existing DICOM Source\n"
curl --request DELETE "http://$1:$2/config/source/ORTHANC" | jq
printf "\nDeleting existing DICOM Destination\n"
curl --request DELETE "http://$1:$2/config/destination/ORTHANC" | jq

printf "\nAdding MONAI Deploy AE Title\n"
curl --request POST "http://$1:$2/config/ae" --header "Content-Type: application/json" --data-raw "{\"name\": \"MONAI-DEPLOY\",\"aeTitle\": \"MONAI-DEPLOY\"}"  | jq
printf "\nAdding DICOM Source\n"
curl --request POST "http://$1:$2/config/source" --header "Content-Type: application/json" --data-raw "{\"name\": \"ORTHANC\",\"hostIp\": \"$4\",\"aeTitle\": \"ORTHANC\"}"  | jq
printf "\nAdding DICOM Destination\n"
curl --request POST "http://$1:$2/config/destination" --header "Content-Type: application/json" --data-raw "{\"name\": \"ORTHANC\",\"hostIp\": \"$4\",\"port\": $5,\"aeTitle\": \"ORTHANC\"}"  | jq
printf "\nListing DICOM Sources\n"
curl -f --request GET "http://$1:$2/config/source" | jq
printf "\nListing DICOM Destinations\n"
curl -f --request GET "http://$1:$2/config/destination" | jq