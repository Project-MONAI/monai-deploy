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

printf "\nAdding DICOM Source\n"
curl -s --request POST 'http://mdig:5000/config/source' --header 'Content-Type: application/json' --data-raw '{"name": "ORTHANC","hostIp": "orthanc","aeTitle": "ORTHANC"}'  | jq
printf "\nAdding DICOM Destination\n"
curl -s --request POST 'http://mdig:5000/config/destination' --header 'Content-Type: application/json' --data-raw '{"name": "ORTHANC","hostIp": "orthanc","port": 1114,"aeTitle": "orthanc"}'  | jq
printf "\nListing DICOM Sources\n"
curl -fs --request GET 'http://mdig:5000/config/source' | jq
printf "\nListing DICOM Destinations\n"
curl -fs --request GET 'http://mdig:5000/config/destination' | jq