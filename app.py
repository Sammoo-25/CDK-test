#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_test.cdk_test_stack import CdkTestStack

from cdk_test.vpc_stack import VPCStack
from cdk_test.security_stack import SecurityStack
from cdk_test.baston_stack import BastionStack
from cdk_test.kms_stack import KMSStack
from cdk_test.s3_stack import S3Stack
from cdk_test.RDS_stack import RDSStack


app = cdk.App()
cdk_test_vpc = VPCStack(app, 'cdk-test-vpc')
security_stack = SecurityStack(app, 'security-stack', vpc=cdk_test_vpc.vpc)
bastion_stack = BastionStack(app, 'bastion', vpc=cdk_test_vpc.vpc, sg=security_stack.bastion_sg)
kms_stack = KMSStack(app, 'kms')
s3_stack = S3Stack(app, 's3buckets')
rds_stack = RDSStack(app, 'rds', vpc=cdk_test_vpc.vpc, lambdasg=security_stack.lambda_sg, bastionsg=security_stack.bastion_sg, kmskey=kms_stack.kms_rds)

app.synth()
