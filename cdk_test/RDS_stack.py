import json
from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_ssm as ssm,
    aws_secretsmanager as sm,
    Stack,
)
from constructs import Construct

class RDSStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, lambdasg: ec2.SecurityGroup,
                 bastionsg: ec2.SecurityGroup, kmskey, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("Project_name")
        env_name = self.node.try_get_context("env")


        json_template = {'username': 'admin'}


        db_creds = sm.Secret(self, 'db_secret',
                             secret_name=env_name + '/rds-secret',
                             generate_secret_string=sm.SecretStringGenerator(
                                 include_space=False,
                                 password_length=12,
                                 generate_string_key='rds-password',
                                 exclude_punctuation=True,
                                 secret_string_template=json.dumps(json_template)
                             )
                             )



        # Define the RDS cluster
        db_mysql = rds.DatabaseCluster(self, id='mysql',
                                       default_database_name=prj_name + env_name,
                                       engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
                                       credentials=rds.Credentials.from_secret(secret=db_creds, username='admin'),  # Add password key here
                                       vpc=vpc,
                                       vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
                                       # instances=1,
                                       storage_encryption_key=kmskey,
                                       writer=rds.ClusterInstance.provisioned(id='writer-inst',
                                                                              instance_type=ec2.InstanceType('t3.micro')),
                                       readers=[rds.ClusterInstance.provisioned('reader-inst-1',
                                                                              instance_type=ec2.InstanceType('t3.micro')),
                                                rds.ClusterInstance.provisioned('reader-inst-2',
                                                                                instance_type=ec2.InstanceType('t3.micro')
                                                                                )
                                                ],

                                       parameter_group=rds.ParameterGroup(self, 'rds-parm-group-id', engine=rds.DatabaseClusterEngine.AURORA_MYSQL),
                                       )

        db_mysql.connections.allow_default_port_from(lambdasg, "Access from Lambda functions")
        db_mysql.connections.allow_default_port_from(bastionsg, "Allow from bastion host")

        ssm.StringParameter(
            self, 'db-host',
            string_value=db_mysql.cluster_endpoint.hostname
        )
