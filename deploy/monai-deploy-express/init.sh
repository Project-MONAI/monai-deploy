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

RUNDIR=$PWD/.md

echo "Initializing directories..."
[ -d $RUNDIR ] && echo "Removing existin $RUNDIR" && sudo rm -r $RUNDIR
mkdir -p $RUNDIR/esdata/ && echo "Created $RUNDIR/"
mkdir -p $RUNDIR/minio/ && echo "Created $RUNDIR/minio/"
mkdir -p $RUNDIR/rabbitmq/ && echo "Created $RUNDIR/rabbitmq/"
mkdir -p $RUNDIR/orthanc/ && echo "Created $RUNDIR/orthanc/"
mkdir -p $RUNDIR/mongodb/ && echo "Created $RUNDIR/mongodb/"
mkdir -p $RUNDIR/mdwm/ && echo "Created $RUNDIR/mdwm/"
mkdir -p $RUNDIR/mdtm/ && echo "Created $RUNDIR/mdtm/"
mkdir -p $RUNDIR/mdig/ && echo "Created $RUNDIR/mdig/"
sudo chown $(id -u):$(id -g) -R $RUNDIR/esdata && echo "Permission updated"
echo "Directories setup"
echo "Ready to run docker compose up"
