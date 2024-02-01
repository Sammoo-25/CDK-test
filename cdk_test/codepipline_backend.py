from aws_cdk import (
    aws_codecommit as code,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cp_actions,
    aws_codebuild as build,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ssm as ssm,
    Stack,
    Aws
)
from constructs import Construct


# import backend_buildspec


class CodePiplineBackendStack(Stack):

    def __init__(self, scope: Construct, id: str, art_bucket_name, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        artifact_bucet = s3.Bucket.from_bucket_name(self, 'artifactbucket', art_bucket_name)
        repo_name = ssm.StringParameter.value_for_string_parameter(self, f'/{env_name}/repo/param/name')
        repo = code.Repository.from_repository_name(self, 'backendrepo', repo_name)


        ## CodeBuild project
        build_project = build.PipelineProject(self, 'buildproject',
                                              project_name=f'{env_name}-build-project',
                                              description='package lambda functions',
                                              environment=build.BuildEnvironment(
                                                  build_image=build.LinuxBuildImage.STANDARD_3_0,
                                              ),
                                              cache=build.Cache.bucket(artifact_bucet, prefix='codebuild-cache'),
                                              build_spec=build.BuildSpec.from_source_filename('buildspec.yml')
                                              )

        ## CodePipeline
        pipeline = cp.Pipeline(self, 'backend-pipeline',
                               pipeline_name=f"{env_name}-backend-pipeline",
                               artifact_bucket=artifact_bucet,
                               restart_execution_on_update=False
                               )

        #Source stage
        source_output = cp.Artifact(artifact_name='source')
        source_action = cp_actions.CodeCommitSourceAction(
            action_name='Source',
            repository=repo,
            output=source_output,
            branch='main'
        )

        pipeline.add_stage(stage_name='Source', actions=[source_action])

        #Build Stage
        build_output = cp.Artifact(artifact_name='build')

        pipeline.add_stage(stage_name='Build',
                           actions=[cp_actions.CodeBuildAction(
                               action_name='Build',
                               input=source_output,
                               project=build_project,
                               outputs=[build_output]
                           )]
                           )

        build_project.role.add_to_principal_policy(iam.PolicyStatement(
            actions=['cloudformation:*', 's3:*', 'iam:*', 'lambda:*', 'apigateway:*', 'ecr:*'],
            resources=['*']
        ))


        account_id = Aws.ACCOUNT_ID
        region = Aws.REGION

        #SSM
        ssm.StringParameter(self, 'account-id',
                            parameter_name=f'/{env_name}/account_id',
                            string_value=account_id
                            )

        ssm.StringParameter(self, 'region',
                            parameter_name=f'/{env_name}/region',
                            string_value=region
                            )
