# The GetItem operation returns a set of attributes for the item with the given primary key. 
# If there is no matching item, GetItem does not return any data and there will 
# be no Item element in the response.


import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Table Name")    # Change

try:
    response = table.get_item(
        Key={
            'id': "value",              # Change
        }
    )

except Exception as e:
    print(e)

else:
    print(response)