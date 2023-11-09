"""
Contains the automation logic to run on the instance first deployment.
SPDX-License-Identifier: Apache 2.0
"""


from constructs import Construct
import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
import aws_cdk.aws_logs as logs
from aws_cdk import (aws_iam as iam )

class userdata(Construct):
    def __init__(self, scope: Construct, id: str,  monaiuser_password: str , **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._userdata = ec2.UserData.for_linux()
        self._userdata.add_commands(
                                    #install Cfn utility
                                    "cd /tmp",
                                    "apt-get update -y",
                                    "apt install python3-pip -y",
                                    "wget https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-py3-latest.tar.gz",
                                    "tar -xvf aws-cfn-bootstrap-py3-latest.tar.gz",
                                    "cd /tmp/aws-cfn-bootstrap-2.0",
                                    "pip install .",
                                    "mkdir -p /opt/aws/bin",
                                    "cd /opt/aws/bin",
                                    "ln -s /usr/local/bin/cfn-* .",
                                    )

        self._userdata.add_commands(    #disabling interactive service restarter 
                                        #"sed -i 's/#$nrconf\{restart\} = \x27i\x27/$nrconf\{restart\} = \x27a\x27/' /etc/needrestart/needrestart.conf",
                                        "touch /tmp/needrestart_silenced",
                                        #create default user
                                        "adduser --gecos \"\" --disabled-password monaiuser",
                                        "chpasswd <<<'monaiuser:"+monaiuser_password+"'",
                                        "usermod -aG sudo monaiuser",
                                        "touch /tmp/monaiuser_created",
                                        #update the OS
                                        "apt update -y",
                                        "apt upgrade -y",
                                        "touch /tmp/OS_upgraded",
                                        #install Docker 
                                        "apt-get remove docker docker.io containerd runc",
                                        "apt-get install ca-certificates curl gnupg lsb-release",
                                        "mkdir -p /etc/apt/keyrings",
                                        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
                                        "echo deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
                                        "sudo apt-get update -y",
                                        "apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin",
                                        "touch /tmp/docker_installed",
                                        #install Docker compose plugin
                                        "apt-get install docker-compose-plugin -y",
                                        "touch /tmp/compose_plugin_installed",
                                        #install Cuda Driver
                                        "cd /tmp",
                                        "wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb",
                                        "dpkg -i cuda-keyring_1.0-1_all.deb",
                                        "apt-get update",
                                        "apt-get -y install cuda",
                                        "touch /tmp/cuda_driver_installed",
                                        #Install nvidia container Toolkit
                                        "curl https://get.docker.com | sh && systemctl --now enable docker",
                                        "distribution=$(. /etc/os-release;echo $ID$VERSION_ID)",
                                        "curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg",
                                        "curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | tee /etc/apt/sources.list.d/nvidia-container-toolkit.list",
                                        "apt-get update -y",
                                        "apt-get install -y nvidia-container-toolkit",
                                        "nvidia-ctk runtime configure --runtime=docker",
                                        "systemctl restart docker",
                                        "docker run --rm  --gpus all nvidia/cuda:11.6.2-base-ubuntu20.04 nvidia-smi",
                                        "touch /tmp/nvidia_toolkit_installed",
                                        #install the MONAI Informatic Gateway CLI
                                        "apt install unzip -y",
                                        "cd /tmp",
                                        "curl -LO https://github.com/Project-MONAI/monai-deploy-informatics-gateway/releases/download/0.4.1/mig-cli-0.4.1-linux-x64.zip",
                                        "unzip ./mig-cli-0.4.1-linux-x64.zip",
                                        "mv mig-cli /usr/local/bin",
                                        "touch /tmp/MIG_installed",
                                        #install MONAI Deploy Express
                                        "cd /tmp",
                                        "curl -LO https://github.com/Project-MONAI/monai-deploy/releases/download/monai-deploy-express-v0.5.0/monai-deploy-express-0.5.0.zip",
                                        "unzip ./monai-deploy-express-0.5.0.zip -d /home/monaiuser",
                                        "chown monaiuser:monaiuser /home/monaiuser/deploy -R",
                                        "touch /tmp/mde_installed",
                                        #iniatialize monai storage
                                        "/home/monaiuser/deploy/monai-deploy-express/init.sh",
                                        "cd /home/monaiuser/deploy/monai-deploy-express",
                                        "docker compose up -d",
                                        #giving a bit of time for the containers to start. Does not really matter if the start is incomplete, the services will reboot at next server restart.
                                        #add monaiuser to docker users group
                                        "groupadd docker",
                                        "usermod -aG docker monaiuser",
                                        "newgrp docker",
                                        "touch /tmp/monaiuser_docker_granted",
                                        #configure crontab to start docker compose at startup
                                        "su -c \" echo \"@reboot sleep 60 && docker compose -f /home/monaiuser/deploy/monai-deploy-express/docker-compose.yml up -d\" > /tmp crontab.save\" monaiuser",
                                        "su -c \" crontab /tmp/crontab.save\" monaiuser"
                                        #Reboot
                                        "reboot"

                                    ) 


    def getUserData(self):
        return self._userdata