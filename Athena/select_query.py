# Excute SQL Query on Athena and display results

import time
import boto3

def fetchall_athena(query_string, client):
    execution_id = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': "Your DataBase" # Change
        },
        ResultConfiguration={
            'OutputLocation':'s3://YourBucket/Path' # Change
        }
    )['QueryExecutionId']


    state = 'RUNNING'

    # Check Query Status
    while (state in ['RUNNING']):
        response = client.get_query_execution(QueryExecutionId = execution_id)

        if 'QueryExecution' in response and \
                'Status' in response['QueryExecution'] and \
                'State' in response['QueryExecution']['Status']:
            state = response['QueryExecution']['Status']['State']
            if state == 'FAILED':
                return False
            elif state == 'SUCCEEDED':
                s3_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
        time.sleep(1)

    #Fetchs Result
    results_paginator = client.get_paginator('get_query_results')
    results_iter = results_paginator.paginate(
        QueryExecutionId=execution_id,
        PaginationConfig={
            'PageSize': 1000
        }
    )

    for results_page in results_iter:
        for row in results_page['ResultSet']['Rows']:
            print(row['Data'])
        

query = 'Your Query'    # Change
client = boto3.client('athena')

fetchall_athena(query,client)