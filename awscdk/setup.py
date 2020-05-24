import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="awscdk",
    version="0.0.1",
    description="Verbose Equals True application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Brian Caffey",
    package_dir={"": "awscdk"},
    packages=setuptools.find_packages(where="awscdk"),
    install_requires=[
        "aws-cdk.core==1.41.0",
        "aws-cdk.aws_certificatemanager==1.41.0",
        "aws-cdk.aws_secretsmanager==1.41.0",
        "aws-cdk.aws_route53==1.41.0",
        "aws-cdk.aws_s3==1.41.0",
        "aws_cdk.aws_s3_deployment==1.41.0",
        "aws-cdk.aws_cloudfront==1.41.0",
        "aws-cdk.aws_route53_targets==1.41.0",
        "aws-cdk.aws_ecr==1.41.0",
        "aws-cdk.aws_ec2==1.41.0",
        "aws-cdk.aws_rds==1.41.0",
        "aws-cdk.aws_ssm==1.41.0",
        "aws-cdk.aws_elasticache==1.41.0",
        "aws-cdk.aws_elasticloadbalancingv2==1.41.0",
        "aws-cdk.aws_ecs==1.41.0",
        "aws-cdk.aws_ecs_patterns==1.41.0",
        "aws-cdk.aws_autoscaling==1.41.0",
        "aws-cdk.aws_sqs==1.41.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
