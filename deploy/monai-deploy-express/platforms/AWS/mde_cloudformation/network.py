"""
Generates VPC, subnets and elastic IP.
SPDX-License-Identifier: Apache 2.0
"""


from constructs import Construct
import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
import aws_cdk.aws_logs as logs
from aws_cdk import (aws_iam as iam )

class network(Construct):
    
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._vpc = ec2.Vpc(  self, 
                        "Vpc",
                        ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/27"),
                        subnet_configuration=[
                                                ec2.SubnetConfiguration(
                                                    subnet_type=ec2.SubnetType.PUBLIC,
                                                    name="Public",
                                                    cidr_mask=28,
                                                ),
                                            ],
                        enable_dns_support=True,
                        enable_dns_hostnames=True
    
                    )
        log_group = logs.LogGroup(self, "MONAIDeployExpress-vpcLogs")
    

        role = iam.Role(self, "MONAIDeployExpress-Flowlogsrole",
            assumed_by=iam.ServicePrincipal("vpc-flow-logs.amazonaws.com")
        )

        ec2.FlowLog(
                    self, 
                    "FlowLog",
                    resource_type=ec2.FlowLogResourceType.from_vpc(self._vpc),
                    destination=ec2.FlowLogDestination.to_cloud_watch_logs(log_group, role)
        )

        self._elastic_ip = ec2.CfnEIP(self, "EIP", domain="vpc" , tags=[cdk.CfnTag(key="Name",value="MONAIDeployExpress-EIP"),])

        self._security_group = ec2.SecurityGroup(self, "MONAIDeployExpress-SecurityGroup" , vpc=self._vpc , allow_all_outbound=True, description="MONAI Deploy Express security group. Allows SSH 22 and DICOM 5000" , security_group_name="MONAIDeployExpress-SG" )

        #This allows the subnets in the peerlist to access to the service.
        self._security_group.add_ingress_rule(peer=ec2.Peer.ipv4('255.255.255.255/32'), connection=ec2.Port.tcp(22), description="SSH access to the MONAI Deploy Express server")
        self._security_group.add_ingress_rule(peer=ec2.Peer.ipv4('255.255.255.255/32'), connection=ec2.Port.tcp(104), description="DICOM DIMSE to MONAI Informatic Gateway")
        self._security_group.add_ingress_rule(peer=ec2.Peer.ipv4('255.255.255.255/32'), connection=ec2.Port.tcp(8042), description="Orthanc server UI access")
        self._security_group.add_ingress_rule(peer=ec2.Peer.ipv4('255.255.255.255/32'), connection=ec2.Port.tcp(4242), description="DICOM DIMSE to Orthanc server") 
        self._security_group.add_ingress_rule(peer=ec2.Peer.ipv4('255.255.255.255/32'), connection=ec2.Port.tcp(5601), description="Kibana server UI access") 


    def getVPC(self) -> ec2.Vpc:
        return self._vpc

    def getEIP(self) -> ec2.CfnEIP:
        return self._elastic_ip

    def getSecurityGroup(self) -> ec2.SecurityGroup:
        return self._security_group