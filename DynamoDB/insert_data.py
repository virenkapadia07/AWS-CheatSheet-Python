# Creates a new item, or replaces an old item with a new item. 
# If an item that has the same primary key as the new item already exists 
# in the specified table, the new item completely replaces the existing item. 
# You can perform a conditional put operation (add a new item if one with the specified primary key doesn't exist), 
# or replace an existing item if it has certain attribute values. 
# You can return the item's attribute values in the same operation,
# using the ReturnValues parameter.

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Table Name")    # Change


# The primary key is required. 
# This code adds an item that has primary key (year, title) and info attributes. 
# The info attribute stores sample JSON that provides more information about the movie. 
response = table.put_item(
   Item={
        'year': year,
        'title': title,
        'info': {
            'plot':"Nothing happens at all.",
            'rating': "7.9"
        }
    }
)

print(response)