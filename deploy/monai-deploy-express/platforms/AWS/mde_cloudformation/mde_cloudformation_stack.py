from aws_cdk import (
    # Duration,
    CfnParameter,
    Stack,
    aws_ec2 as ec2
    # aws_sqs as sqs,
)
from constructs import Construct
from .network import network
from .instance import instance
from .userdata import userdata
from .cloudformationInit import cloudformationInit

class MdeCloudformationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        monaiuser_password = CfnParameter(self , "monaiuser_password" , type="String" , no_echo=True , min_length=8 , description="Must be 8 charactersor or more, contain uper case, lower case and special characters." , constraint_description="Must be 8 charactersor or more, contain uper case, lower case and special characters." , allowed_pattern="^.*(?=.{8,120})(?!.*\s)(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\!\@\#\$\%\^\&\*\(\)\-\=\¡\£\_\+\`\~\.\,\<\>\/\?\;\:\'\"\\\|\[\]\{\}]).*$" )
        network_config = network(self , "mde-network")
        user_data = userdata(self, "userdata" , monaiuser_password=monaiuser_password.value_as_string)
        cfninit = cloudformationInit(self, "InitScript")
        ec2instance = instance(self , "mde-instance" , vpc=network_config.getVPC() , security_group=network_config.getSecurityGroup() , user_data=user_data.getUserData() , cfn_init = cfninit.getCfnInit() , cfn_init_options=cfninit.getCfnInitOptions())
        ec2.CfnEIPAssociation(self,"MONAIDeployExpress-EIP", eip=network_config.getEIP().attr_public_ip , instance_id=ec2instance.getInstance().instance_id)

