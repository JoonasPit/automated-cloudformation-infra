
from troposphere import Output, Ref, Template
from troposphere.s3 import Bucket, Private
import sys

t = Template()

bucket_name="akefalos-lambda-bucket"

s3bucket = t.add_resource(
    Bucket(
        "AkefalosSecondBucket",
        BucketName=bucket_name,
        AccessControl=Private,
    )
)


t.add_output(
    Output(
        "AkefalosSecondBucket",
        Value=Ref(s3bucket),
        Description="Name"

    )
)

print(t.to_json())