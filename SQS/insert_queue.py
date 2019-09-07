# Delivers a message to the specified queue

import boto3

sqs = boto3.client('sqs')
queue_url = "YOUR QUEUE URL"    # Change

def InsertQueue(data):
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': 'YOUR DATA'  # Change
                },
                'Author': {
                    'DataType': 'String',
                    'StringValue': 'Author Name'    # Change
                }
            },
            MessageBody=(
                data  # Change
            ),
            MessageGroupId="Your Group ID"  # Change
        )
    except Exception as e:
        print("[+] ######### Exception while Inserting Queue #########")
        print(e)
        
        return False
    else:
        return True