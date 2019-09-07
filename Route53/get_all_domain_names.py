# Lists the resource record sets in a specified hosted zone.

import boto3

client = boto3.client('route53')

HOST_NAME=[]

# ListResourceRecordSets returns up to 100 resource 
# record sets at a time in ASCII order, beginning at a 
# position specified by the name and type elements.
response = client.list_resource_record_sets(
    HostedZoneId='YOUR HOSTED ID',      # Change
)

for records in response["ResourceRecordSets"]:
    HOST_NAME.append(records["Name"][:-1])


while response["IsTruncated"]:
    response = client.list_resource_record_sets(
        HostedZoneId='YOUR HOSTED ID',      # Change
        StartRecordName=response["NextRecordName"],
        StartRecordType=response["NextRecordType"]
    )

    for records in response["ResourceRecordSets"]:
        HOST_NAME.append(records["Name"])