from typing import Type
from troposphere import GetAtt, ImportValue, Template, Ref, Join, Output
from troposphere.apigateway import ApiKey, ApiStage, EndpointConfiguration, Integration, Resource, RestApi, Method, Deployment,Stage, StageKey, UsagePlan, UsagePlanKey
from troposphere.iam import Role, Policy
from os import getenv
t = Template()

lambda_arn = ImportValue("AkefalosLambdaArn")
region = getenv("REGION")
environment = getenv("ENV_NAME")

## LAMBDA PROXY NEEDS TO BE TURNED ON
akefalos_api = t.add_resource(
    RestApi(
        "AkefalosApi",
        Name="AkefalosApi",
        EndpointConfiguration=EndpointConfiguration(
            Types=["REGIONAL"]
        )
    )
)


# Gateway role to execute api
api_lambda_execution_role = t.add_resource(
    Role(
        "ApiLambdaRole",
        Path="/",
        Policies=[
            Policy(
                PolicyName="root",
                PolicyDocument={
                    "Version" : "2012-10-17",
                    "Statement": 
                    [
                         {
                            "Action": ["lambda:*"], 
                            "Resource": "*", 
                            "Effect": "Allow"
                         },

                    ]
                }           
            )
        ],
        AssumeRolePolicyDocument={
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": ["sts:AssumeRole"],
                    "Effect": "Allow",
                    "Principal": {
                        "Service": ["lambda.amazonaws.com", "apigateway.amazonaws.com"]
                    },
                }
            ],
        }
    )
)

akefalos_api_resource = t.add_resource(
    Resource(
        "AkefalosResource",
        RestApiId=Ref(akefalos_api),
        PathPart="run",
        ParentId=GetAtt("AkefalosApi", "RootResourceId")
    )
)

akefalos_method = t.add_resource(
    Method(
        "AkefalosLambdaMethod",
        RestApiId=Ref(akefalos_api),
        ApiKeyRequired=True,
        AuthorizationType="NONE",
        ResourceId=Ref(akefalos_api_resource),
        HttpMethod="GET",
        Integration=Integration(
            Credentials= GetAtt(api_lambda_execution_role, "Arn"),
            Type="AWS_PROXY",
            Uri=Join(
                "",
                [f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/", # This is standard - region should be paramed
                lambda_arn,"/invocations"]
            ),
            IntegrationHttpMethod="POST", #Should be post when posting to a backend service

        )
    )
)

akefalos_api_deployment = t.add_resource(
    Deployment(
        f"Akefalos{environment}Deployment",
        DependsOn=akefalos_method,
        RestApiId=Ref(akefalos_api)

    )
)

stage = t.add_resource(
    Stage(
        f"Akefalos{environment}Stage",
        StageName=f"{environment}",
        RestApiId=Ref(akefalos_api),
        DeploymentId=Ref(akefalos_api_deployment)
    )
)

akefalos_api_key = t.add_resource(
    ApiKey(
        "ApiKey",
         StageKeys=[
             StageKey(
             RestApiId=Ref(akefalos_api), StageName=Ref(stage)
             )
             ]
    )
)

akefalos_usage_plan = t.add_resource(
    UsagePlan(
        "ExampleUsagePlan",
        UsagePlanName="ExampleUsagePlan",
        Description="Example usage plan",
        ApiStages=[
            ApiStage(
                ApiId=Ref(akefalos_api),
                Stage=Ref(stage),
            )
        ],
    )
)

# tie the usage plan and key together
usagePlanKey = t.add_resource(
    UsagePlanKey(
        "UsagePlanKey",
        KeyId=Ref(akefalos_api_key),
        KeyType="API_KEY",
        UsagePlanId=Ref(akefalos_usage_plan),
    )
)


t.add_output(Output("ApiKey", Value=Ref(akefalos_api_key), Description="API key"))

print(t.to_json())