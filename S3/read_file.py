# Retrieves/ Download objects(files) from Amazon S3.

import boto3

s3 = boto3.client('s3')

bucket = "Your Bucket Name"         # Change
object_key = "YourPath/filename"    # Change

def S3_Read():
    response = s3.get_object(Bucket=bucket, Key=object_key)
    data = response['Body']
    data = data.read().decode('utf-8')

    return data