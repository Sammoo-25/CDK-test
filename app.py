#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_test.cdk_test_stack import CdkTestStack
from aws_cdk import Fn
from cdk_test.vpc_stack import VPCStack
from cdk_test.security_stack import SecurityStack
from cdk_test.baston_stack import BastionStack
from cdk_test.kms_stack import KMSStack
from cdk_test.s3_stack import S3Stack
from cdk_test.RDS_stack import RDSStack
from cdk_test.redis_stack import RedisStack
from cdk_test.cognito_stack import CognitoStack
from cdk_test.apigt_stack import APIStack
from cdk_test.lambda_stack import LambdaStack
from cdk_test.commit_stack import CodeCommitStack
from cdk_test.codepipline_backend import CodePiplineBackendStack
from cdk_test.ecr_stack import ECRStack
from cdk_test.cdn_stack import CDNStack
from cdk_test.acm_stack import ACMStack
from cdk_test.codepipeline_frontend import CodePiplineFrontendStack


app = cdk.App()
cdk_test_vpc = VPCStack(app, 'cdk-test-vpc')
security_stack = SecurityStack(app, 'security-stack', vpc=cdk_test_vpc.vpc)
bastion_stack = BastionStack(app, 'bastion', vpc=cdk_test_vpc.vpc, sg=security_stack.bastion_sg)
kms_stack = KMSStack(app, 'kms')
s3_stack = S3Stack(app, 's3buckets')
rds_stack = RDSStack(app, 'rds', vpc=cdk_test_vpc.vpc, lambdasg=security_stack.lambda_sg, bastionsg=security_stack.bastion_sg, kmskey=kms_stack.kms_rds)
redis_stack = RedisStack(app, 'redis', vpc=cdk_test_vpc.vpc, redissg=Fn.import_value('redis-sg-export'))
cognito_stack = CognitoStack(app, 'cognito')
api_gw_stack = APIStack(app, 'api-gw')
lambda_stack = LambdaStack(app, 'lambda')

commit_repo = CodeCommitStack(app, 'code-commit')
ecr_repo = ECRStack(app, 'ecr')

cp_backend = CodePiplineBackendStack(app, 'cp-backend', art_bucket_name=Fn.import_value('build-artifacts-bucket'))

#Frontend
cdn_stack = CDNStack(app, 'cdn', s3bucket=Fn.import_value('frontend-bucket'))
acm_stack = ACMStack(app, 'acm')
cp_frontend = CodePiplineFrontendStack(app,'cp-frontend', webhostingbucket=Fn.import_value('frontend-bucket'))

app.synth()
