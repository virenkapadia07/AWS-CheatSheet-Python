# Retrieves one or more messages (up to 10), 
# from the specified queue. Using the WaitTimeSeconds parameter enables long-poll support

import boto3

sqs = boto3.client('sqs')
queue_url = "YOUR QUEUE URL"    # Change


def ReadQueue():
    try:
        response = sqs.receive_message(
                QueueUrl=queue_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=10,     # 1-10
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=350,      # Can be set according to your requirements
                WaitTimeSeconds=0
            )
        
    except Exception as e:
        print("[+] Exception Occured")
        print(str(e))

        return False
    else:
        if 'Messages' in response.keys():
            for data in response["Messages"]:
                body = data["Body"]
                receipt_id = data["ReceiptHandle"]

                print("Data:", body)
                print("Receipt Id:",receipt_id)
                
        return True
                