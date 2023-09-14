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

COUNT=${2:-1}
FILES=$(ls -1 $1 | wc -l)
for (( c=1; c<=${COUNT}; c++ ))
do 
    echo Sending $FILES from $1 to MONAI-DEPLOY
    storescu -v +sd +II +IR $FILES -aec MONAI-DEPLOY localhost 104 $1
    echo "Sleeping for 20s"
    sleep 20
done