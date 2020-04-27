from aws_cdk import aws_iam as iam, aws_s3 as s3, core


class Assets(core.Construct):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.assets_bucket = s3.Bucket(self, "AssetsBucket")

        self.policy_statement = iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"{self.assets_bucket.bucket_arn}/static/*"],
        )

        self.policy_statement.add_any_principal()

        self.static_site_policy_document = iam.PolicyDocument(
            statements=[self.policy_statement]
        )

        self.assets_bucket.add_to_resource_policy(self.policy_statement)
