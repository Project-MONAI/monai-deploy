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
echo "Informatics Gateway Host Name = $1"
echo "Informatics Gateway Port      = $2"
echo "Orthanc IP Address            = $3"
echo "Orthanc SCP Port              = $4"
echo -e "\n"

printf "\nAdding MONAI Deploy AE Title\n"
curl --request POST "http://$1:$2/config/ae" --header "Content-Type: application/json" --data-raw "{\"name\": \"MONAI-DEPLOY\",\"aeTitle\": \"MONAI-DEPLOY\"}"  | jq
printf "\nAdding DICOM Source\n"
curl --request POST "http://$1:$2/config/source" --header "Content-Type: application/json" --data-raw "{\"name\": \"ORTHANC\",\"hostIp\": \"$3\",\"aeTitle\": \"ORTHANC\"}"  | jq
printf "\nAdding DICOM Destination\n"
curl --request POST "http://$1:$2/config/destination" --header "Content-Type: application/json" --data-raw "{\"name\": \"ORTHANC\",\"hostIp\": \"$3\",\"port\": $4,\"aeTitle\": \"ORTHANC\"}"  | jq
printf "\nListing DICOM Sources\n"
curl -f --request GET "http://$1:$2/config/source" | jq
printf "\nListing DICOM Destinations\n"
curl -f --request GET "http://$1:$2/config/destination" | jq