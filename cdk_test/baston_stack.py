from aws_cdk import (
    aws_ec2 as ec2,
    Stack,
)
from constructs import Construct


class BastionStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        key_name = ec2.CfnKeyPair(self, 'Bastion_key',
                                  key_name='BastionKey'
                                  )

        baston_host = ec2.Instance(self, 'baston-host',
                                   instance_type=ec2.InstanceType('t3.micro'),
                                   machine_image=ec2.AmazonLinuxImage(
                                       edition=ec2.AmazonLinuxEdition.STANDARD,
                                       generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                       virtualization=ec2.AmazonLinuxVirt.HVM,
                                       storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                   ),
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(
                                       subnet_type=ec2.SubnetType.PUBLIC
                                   ),
                                   security_group=sg
        )
