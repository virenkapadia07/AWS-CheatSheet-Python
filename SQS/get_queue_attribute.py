# Gets attributes for the specified queue.

import boto3

client = boto3.client('sqs')

queue_url = 'Your Queue URL'    # Change

response = client.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=[
        'ApproximateNumberOfMessages','ApproximateNumberOfMessagesNotVisible'
    ]
)

message_available=response['Attributes']['ApproximateNumberOfMessages']
message_in_flight=response['Attributes']['ApproximateNumberOfMessagesNotVisible']