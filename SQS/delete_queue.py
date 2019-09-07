# Deletes up to ten messages from the specified queue. 
# The result of the action on each message is reported individually in the response.

import boto3

sqs = boto3.client('sqs')
queue_url = "YOUR QUEUE URL"    # Change

def DeleteQueue(id, receipt_id):
    try:
        dq_response = sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_id
        )
    except Exception as e:
        print("[+] ######### Exception while Deleting Queue #########")
        print(str(e))
        
        return False
    else:
        print(f"[+] Queue Deleted Successfully for {id}")

        return True
