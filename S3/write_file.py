# Adds an object(file) to a bucket.

import boto3

s3 = boto3.client('s3')

bucket = "Your Bucket Name"         # Change
object_key = "YourPath/filename"    # Change

def S3_Write(content):
    if content:
        s3 = boto3.resource('s3')
        response = s3.Object(bucket, object_key).put(Body=content.encode())
        print("File Stored on S3")