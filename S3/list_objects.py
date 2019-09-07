# Returns some or all (up to 1000) of the objects in a bucket. 
# You can use the request parameters as selection criteria to 
# return a subset of the objects in a bucket.

import boto3

s3 = boto3.client('s3')

bucket = "Your Bucket Name"  # Change
prefix = 'path/'  # Change

result = s3.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')

for r in result['CommonPrefixes']:  # Get 1000 lists 
    print(r["Prefix"])

while result["IsTruncated"]:
    # S3 Lists first 1000 list per request
    # If you want all list than use While loop
    result = s3.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/',Marker=result["NextMarker"])
    for r in result['CommonPrefixes']:
            prit(r["Prefix"])