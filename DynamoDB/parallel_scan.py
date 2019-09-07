# Perform Parallel Scan on DynamoDB to retrive record fast
# The Scan operation returns one or more items and item attributes by 
# accessing every item in a table or a secondary index. 
# To have DynamoDB return fewer items, you can provide a FilterExpression operation.
# Scan operations proceed sequentially; however, 
# for faster performance on a large table or secondary index, 
# applications can request a parallel Scan operation by providing the Segment and TotalSegments parameters.


import threading
import boto3
from boto3.dynamodb.conditions import Key, Attr
from multiprocessing import Pool

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Table Name')


def read_data(segment):
    # Scan 100 rows only
    response = table.scan(
            ProjectionExpression="Name of Columns You want",
            FilterExpression= "Scan Based on condition",  # Key("column name").eq("value"),  #Can Add more than one conition using &
            Segment=segment,
            TotalSegments=10,
            )
    # Parallel Scan: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.ParallelScan

    if response["Items"]:
        print(response["Items"])
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(
        ProjectionExpression="Name of Columns You want",
        FilterExpression= "Scan Based on condition",  # Key("column name").eq("value"),  #Can Add more than one conition using &
        ExclusiveStartKey=response['LastEvaluatedKey'],
        Segment=segment,
        TotalSegments=10
        )

        if response["Items"]:
            print(response["Items"])



# Can increase processes as per your requirement
process_no = 10

p = Pool(processes=process_no)  
segments = range(1,process_no)
result = p.map(read_data, segments)