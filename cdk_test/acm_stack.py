from aws_cdk import (
    Stack,
    aws_ssm as ssm,
    aws_route53 as r53,
    aws_certificatemanager as acm
)
# from aws_cdk.aws_certificatemanager import (
#     Certificate as cert,
#     ValidationMethod as val_met
# )

from constructs import Construct


class ACMStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("Project_name")
        env_name = self.node.try_get_context("env")

        hosted_zone = r53.HostedZone.from_lookup(self, 'hosted-zone-id')

        certificate = acm.Certificate(self, 'Certificate',
                        domain_name='cdk-test-api.academy.goya.am',
                        certificate_name='cdk-course-cert',
                        validation=acm.CertificateValidation.from_dns(hosted_zone)
                        )
        # SSM
        ssm.StringParameter(self, 'acm-param',
                            parameter_name=f'/{env_name}/acm/param/arn',
                            string_value=certificate.certificate_arn
                            )