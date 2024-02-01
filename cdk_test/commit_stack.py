from aws_cdk import (
    aws_ssm as ssm,
    aws_codecommit as cocm,
    Stack,
)
from constructs import Construct

class CodeCommitStack(Stack):
    def __init__(self, scope: Construct, id: str,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("Project_name")
        env_name = self.node.try_get_context("env")


        repo = cocm.Repository(self, 'test-repo-pip',
                               repository_name=f'{prj_name}-{env_name}test-repo'
                               )


        #SSM
        ssm.StringParameter(self, 'repo-arn',
                            parameter_name=f'/{env_name}/repo/param/name',
                            string_value=repo.repository_name
                            )