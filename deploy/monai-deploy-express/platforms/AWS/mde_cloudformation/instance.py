"""
Generates the instance and automate the deployment.
SPDX-License-Identifier: Apache 2.0
"""


from constructs import Construct
import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
import aws_cdk.aws_logs as logs
from aws_cdk import (aws_iam as iam )

class instance(Construct):
    def __init__(self , scope: Construct , id: str , vpc: ec2.Vpc , security_group: ec2.SecurityGroup , user_data: ec2.UserData , cfn_init: ec2.CloudFormationInit , cfn_init_options: ec2.ApplyCloudFormationInitOptions , **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        machineImage = ec2.MachineImage.from_ssm_parameter(
                                parameter_name = '/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id',
                                os =  ec2.OperatingSystemType.LINUX
                            )

        cfn_key_pair = ec2.CfnKeyPair(      self, 
                                            "MyCfnKeyPair",
                                            key_name="MONAIDeployExpress-"+cdk.Fn.ref("AWS::StackId"),
                                            # the properties below are optional
                                            key_type="rsa",
                                            tags=[cdk.CfnTag(
                                                key="Name",
                                                value="MONAIDeployExpress-KeyPair"
                                            )]
                                    )
        instance_role = iam.Role(   self, 
                                    "Role",
                                    assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                                    description="MONAI Deploy Express EC2 instance role."
                                )

        instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        self._instance = ec2.Instance(self, 
                            'MONAIDeployExpress-instance',
                            instance_type=ec2.InstanceType.of(ec2.InstanceClass.G4DN , ec2.InstanceSize.XLARGE),
                            instance_name='MONAIDeployExpress',
                            machine_image=machineImage,
                            vpc=vpc,
                            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                            security_group=security_group,
                            user_data= user_data,
                            key_name=cfn_key_pair.key_name,
                            block_devices=[ec2.BlockDevice(
                                                            device_name="/dev/sda1",
                                                            volume=ec2.BlockDeviceVolume.ebs(volume_size=200, encrypted=True , volume_type=ec2.EbsDeviceVolumeType.GP3)
                                                        ),],
                            role=instance_role,
                            init=cfn_init,
                            init_options=cfn_init_options

                            )

    def getInstance(self) -> ec2.Instance:
        return self._instance