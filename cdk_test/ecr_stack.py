from aws_cdk import (
    aws_ssm as ssm,
    aws_ecr as ecr,
    Stack,
)
from constructs import Construct


class ECRStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("Project_name")
        env_name = self.node.try_get_context("env")

        repo = ecr.Repository(self, 'backend-repo',
                              repository_name='ecs-task-repo',
                              )

        # SSM
        ssm.StringParameter(self, 'repo-param-name',
                            parameter_name=f'/{prj_name}/backend/repo/param',
                            string_value=repo.repository_name
                            )
