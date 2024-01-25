from aws_cdk import (
    aws_ec2 as ec2,
    aws_ssm as ssm,
    Stack,

)
from constructs import Construct


class VPCStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("Project_name")
        env_name = self.node.try_get_context("env")

        self.vpc = ec2.Vpc(self, 'devVPC',
                           # cidr="172.32.0.0/16",
                           ip_addresses=ec2.IpAddresses.cidr("172.32.0.0/16"),
                           max_azs=2,
                           enable_dns_hostnames=True,
                           enable_dns_support=True,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name="Public",
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name="Private",
                                   subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name="Isolated",
                                   subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                                   cidr_mask=24
                               ),
                           ],
                           )
        ssm.StringParameter(self, 'VPCIdParameter',
                            string_value=self.vpc.vpc_id,
                            parameter_name=f'/{env_name}/VPCId'
                            )