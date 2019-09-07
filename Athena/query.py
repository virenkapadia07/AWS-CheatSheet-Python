#  Runs the SQL query statements contained in the Query . 
#  Requires you to have access to the workgroup in which the query ran.

import boto3
import time

athena = boto3.client('athena')
bucket = "Your Bucket"  # Change
path = "Your Path"  # Change
query = "Your Query"    # Change

def ExcuteQuery(query, prop):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': 'Your Database Name'     # Change
        },
        ResultConfiguration={
            'OutputLocation': f's3://{bucket}/{path}'       # Athena Requires S3 path for store query results
        }
    )

    print(response)
    CheckQueryStatus(response['QueryExecutionId'])

def CheckQueryStatus(execution_id):
    # Check Query Status Executed Successfully or not
    
    state = 'RUNNING'

    while (state in ['RUNNING']):
        response = athena.get_query_execution(QueryExecutionId = execution_id)
        if 'QueryExecution' in response and \
                'Status' in response['QueryExecution'] and \
                'State' in response['QueryExecution']['Status']:
            state = response['QueryExecution']['Status']['State']
            if state == 'FAILED':
                print(response)
                print("Query Execution Failed")
            elif state == 'SUCCEEDED':
                print("Query Execution Succeeded")
                print(response)
        time.sleep(1)