
from troposphere import GetAtt, ImportValue,Template, Output, Export, Ref
from troposphere import awslambda
from troposphere.iam import Role

from awacs.aws import Allow, PolicyDocument, Principal, Statement
from awacs.sts import AssumeRole
import os

t = Template()
os.getenv("REGION")
lambda_bucket_name = ImportValue('AkefalosSecondBucket')

lambda_role = t.add_resource(Role(
    "LambdaExecutionRole",
    AssumeRolePolicyDocument=PolicyDocument(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[AssumeRole],
                Principal=Principal("Service", "lambda.amazonaws.com")
            )
        ]
    )
))

akefalos_first_lamdba = t.add_resource(awslambda.Function(
    "AkefalosLambda",
    Code=awslambda.Code(
        S3Bucket=lambda_bucket_name,
        S3Key="hello.zip"
    ),
    Runtime="go1.x",
    Role=GetAtt(lambda_role,"Arn"),
    Handler="hello" ## This needs to be set to built zip name -ie go build foo -> this is foo
    # If need to execute specific function foo.Function would work
))
t.add_output(Output(
        "AkefalosLambdaArn",
        Value=GetAtt(akefalos_first_lamdba, "Arn"),
        Description="Arn",
        Export=Export("AkefalosLambdaArn")

))
print(t.to_json())