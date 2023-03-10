from aws_cdk import (
    # Duration,
    CfnParameter,
    Duration,
    Stack, 
    # aws_sqs as sqs,
)
import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from .network import network
from .instance import instance
from .userdata import userdata

class cloudformationInit(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._cfnInit = ec2.CloudFormationInit.from_elements(
            ec2.InitCommand.shell_command("touch /tmp/Init_done")
        )

        self._init_options=ec2.ApplyCloudFormationInitOptions(
                timeout=Duration.minutes(60)
        )

    def getCfnInit(self):
        return self._cfnInit

    def getCfnInitOptions(self):
        return self._init_options       