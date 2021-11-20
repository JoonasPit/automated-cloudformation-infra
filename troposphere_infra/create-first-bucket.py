
from troposphere import Output, Ref, Template
from troposphere.s3 import Bucket, Private
import sys

t = Template()
output_file = sys.argv[1]
output_folder=sys.argv[2]

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
with open(f"{output_folder}/{output_file}", "w") as file:
    file.write(t.to_json())