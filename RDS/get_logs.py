# Downloading RDS logs
# Downloads all or a portion of the specified log file,

import boto3
import os
from multiprocessing import Pool
from botocore.exceptions import ClientError

client = boto3.client('rds')

def GetLogs(filename):
    f_name=filename.split("/")[1]
    with open(f"{instance}/{f_name}", 'w') as f:
        print('[+] downloading {rds} log file {file}'.format(rds=instance, file=filename))
        token = '0'
        try:
            response = client.download_db_log_file_portion(
                DBInstanceIdentifier=instance,
                LogFileName=filename,
                Marker=token)
            while response['AdditionalDataPending']:
                f.write(response['LogFileData'])
                token=response['Marker']
                response = client.download_db_log_file_portion(
                    DBInstanceIdentifier=instance,
                    LogFileName=filename,
                    Marker=token)
            f.write(response['LogFileData'])
        except ClientError as e:
            # print(e)
            print("[+] Error in downloading:",filename)

file = "File Name"      # Change

# eg. slowquery/mysql-slowquery.log.2019-07-09
# It will download all the logs slowquery/mysql-slowquery.log.2019-07-09.00, 
# slowquery/mysql-slowquery.log.2019-07-09.01...

instance = "InstanceName"   # Change


# fetch db log filename
res = client.describe_db_log_files(
    DBInstanceIdentifier=instance,
    FilenameContains=file
)

try:
    #Make folder 
    os.system(f"mkdir {instance}")
except:
    pass
else:
    p = Pool(processes=10)
    p.map(GetLogs,[x["LogFileName"] for x in res["DescribeDBLogFiles"]])