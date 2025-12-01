import json
import requests
import boto3
import uuid

def lambda_handler(event, context):
    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('inventory')

    # Generate a unique ID
    unique_id = str(uuid.uuid4())

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                '_id': unique_id,
                'Date': data['Date'],
                'Event': data['Event'],
                'Description': data['Description'],
                'Location': data['Location']
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }