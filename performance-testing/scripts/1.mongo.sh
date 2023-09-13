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

NAMESPACE=${1:-default}
export MONGO_PORT=$(kubectl get --namespace $NAMESPACE service/mongo -o jsonpath="{.spec.ports[0].nodePort}")
OUTFILE=$(mktemp)
docker run --network host --rm -it rtsp/mongosh mongoexport "mongodb://localhost:$MONGO_PORT/InformaticsGateway" --quiet --jsonArray --type=json --pretty -c DicomAssociationInfo --authenticationDatabase admin -u monai -p monai > $OUTFILE

COUNTER=1
for row in $(cat $OUTFILE | jq -r '.[] | @base64'); do
    _jq() {
        echo ${row} | base64 --decode | jq -r "${1}"
    }
    _jqdate() {
        echo ${row} | base64 --decode | jq -r "${1} | .[]"
    }

    if [ ! -z "$(echo $row | base64 --decode | jq -r .Errors)" ]; then
        echo "Skipping $(_jq '.CorrelationId') due to errors $(_jq '.Errors')"
        continue
    fi 
    echo "$COUNTER. $(_jq '.CorrelationId')"
    echo "   Duration: $(_jq '.Duration')"
    echo "   Start: $(_jqdate '.DateTimeCreated')"
    echo "   End: $(_jqdate '.DateTimeDisconnected')"
    let COUNTER=COUNTER+1
    echo "==========================================================================================="
    CORRELATIONID=$(_jq '.CorrelationId')
    ./2.perf.sh $CORRELATIONID
    echo "==========================================================================================="
done
