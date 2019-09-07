# Running Select Query on Athena and Downloading the Output from S3 and storing in a file on local

import boto3
import re
import time
from botocore.exceptions import ClientError

query = """ Your Select Query """   # Change

params = {
    'database': 'Your DataBase Name',
    'bucket': 'S3 Bucket',
    'path': 'Path',
    'query':query
}       # Change

session = boto3.Session()

def athena_query(client, params):
    # Excuting Athena query
    response = client.start_query_execution(
        QueryString=params["query"],
        QueryExecutionContext={
            'Database': params['database']
        },
        ResultConfiguration={
            'OutputLocation': 's3://' + params['bucket'] + '/' + params['path']
        }
    )
    return response


def athena_to_s3(session, params):
    # Getting QueryExcutionId for retriving the query
    client = session.client('athena')
    execution = athena_query(client, params)
    execution_id = execution['QueryExecutionId']
    state = 'RUNNING'

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
                filename = re.findall('.*\/(.*)', s3_path)[0]

                return filename
        time.sleep(1)
    
    return False


def cleanup(session, params):
    # Deleting the result(csv file) from s3
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(params['bucket'])
    for item in my_bucket.objects.filter(Prefix=params['path']):
        item.delete()

def CheckFiles(results):
    # Writing into File on Local
    print("Writing into file")
    f = open("result.txt",'w')
    for result in results:
            f.write(result)
            f.write("\n")
    f.close()

if __name__=="__main__":
    filename=athena_to_s3(session,params)
    print(filename)
    if filename:
        time.sleep(15)  # It takes some time to store output in S3
        result=""
        try:
            print("Getting Data from S3")
            s3 = boto3.client('s3')
            object_key = f'{params["path"]}/{filename}'
            response = s3.get_object(Bucket=params["bucket"], Key=object_key)
            body = response['Body']
            data = body.read().decode('utf-8')

        except:
            print("[+] Error occured while reading data from s3")
        else:
            print("Data Retrived from S3")
            CheckFiles(data)
            cleanup(session,params) # Optional    This Function will Delete output file from S3
            print("Done")
    else:
        print("[+] Error occured while reading data from Athena")