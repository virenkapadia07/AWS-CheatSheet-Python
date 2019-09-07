# Edits an existing item's attributes, 
# or adds a new item to the table if it does not already exist. 
# You can put, delete, or add attribute values. 
# You can also perform a conditional update on an 
# existing item (insert a new attribute name-value pair if it doesn't exist, 
# or replace an existing name-value pair if it has certain expected attribute values)


import boto3
from boto3.dynamodb.types import Binary

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Table Name")    # Change

update_data=table.update_item(
    Key={
        'key_1': "key_value_1",     # Change
        'key_2': "key_value_2"      # Change
    },
    UpdateExpression='SET col_n_1 = :val1,col_n_2 = :val2,col_n_3 = :val3,col_n_4 = :val4',
    ExpressionAttributeValues={
        ':val1': col_d_1,
        ':val2': col_d_2,
        ':val3': col_d_3,
        ':val4': Binary(col_d_4),   # If Data to be stored is binary
    }
)