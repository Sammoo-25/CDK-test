from aws_cdk import (
    aws_s3 as s3,
    aws_ssm as ssm,
    Aws,
    RemovalPolicy,
    CfnOutput,
    Stack,
)
from constructs import Construct


class S3Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("Project_name")
        env_name = self.node.try_get_context("env")

        account_id = Aws.ACCOUNT_ID
        lambda_bucket = s3.Bucket(self, 'lambda-bucket',
                                  access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                  encryption=s3.BucketEncryption.S3_MANAGED,
                                  bucket_name='cdk-test-bucket-for-lambda',
                                  block_public_access=s3.BlockPublicAccess(
                                      block_public_acls=True,
                                      block_public_policy=True,
                                      ignore_public_acls=True,
                                      restrict_public_buckets=True
                                  ),
                                  removal_policy=RemovalPolicy.RETAIN
                                  )



        ssm.StringParameter(self, 'ssm-lambda-bucket',
                            parameter_name='/' + env_name + '/lambda-s3-bucket',
                            string_value=lambda_bucket.bucket_name
                            )

        #TO Store Build Artfiacts

        artifacts_buckt = s3.Bucket(self, "build-artifacts",
                                    access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                    encryption=s3.BucketEncryption.S3_MANAGED,
                                    bucket_name=account_id+'-'+env_name+'-build-artifacts',
                                    block_public_access=s3.BlockPublicAccess(
                                        block_public_policy=True,
                                        block_public_acls=True,
                                        ignore_public_acls=True,
                                        restrict_public_buckets=True
                                    ),
                                    removal_policy=RemovalPolicy.DESTROY
        )

        CfnOutput(self, 's3-build-artifacts-export',
                  value=artifacts_buckt.bucket_name,
                  export_name='build-artifacts-bucket'
                  )






