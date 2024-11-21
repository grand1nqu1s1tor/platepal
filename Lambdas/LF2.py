import requests
import json
import boto3
def sendEmail(message):
    client = boto3.client('ses', region_name='us-east-1')
    response = client.send_email(
            Destination={
                'ToAddresses': ['naman.soni@nyu.edu']
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': message,
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Test email',
                },
            },
            Source='naman.soni@nyu.edu'
            )
    print(response)
    return response
def getDataFromDynamo(id):
    table_name = 'yelp-restaurants'
    # Initialize the DynamoDB client
    dynamodb = boto3.client('dynamodb')

    try:
        # Get item from DynamoDB
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'id': {'S': id}  # Assuming the ID is a string
            }
        )
        
        # Extract data from the response
        item = response.get('Item')

        if item:
            # Process the item
            return item
        else:
            return {
                'statusCode': 404,
                'body': 'Item not found'
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
def getDataFromDynamoEmail(email):
    table_name = 'extra-credit-history'
    # Initialize the DynamoDB client
    dynamodb = boto3.client('dynamodb')

    try:
        # Get item from DynamoDB
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'email': {'S': email}  # Assuming the ID is a string
            }
        )
        
        # Extract data from the response
        item = response.get('Item')

        if item:
            # Process the item
            return item
        else:
            return "not found"
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
def getFromES(cuisineType):
    es_endpoint = 'https://search-restaurant-jv5qmadw254con55bfymtebw7i.us-east-1.es.amazonaws.com'

    index = 'restaurants'

    query = {
        "size": 3,
        "query": {
            "function_score": {
                "query": {"match": {"Cuisine": cuisineType}},
                "random_score": {}
            }
        }
    }

    auth = ("your_username", "your_password")

    response = requests.post(f'{es_endpoint}/{index}/_search',
                             json=query,
                             auth=auth)

    if response.status_code == 200:
        es_data = response.json()
        restaurantIDs = []
        for element in es_data['hits']['hits']:
            restaurantIDs.append(element['_source']['RestaurantID'])
        return restaurantIDs
    else:
        return {
            'statusCode': response.status_code,
            'body': response.text
        }

def lambda_handler(event, context):

    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/211125538864/Q1'
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )
    print(response)
    
    # Check if messages are received
    if 'Messages' in response:
        for message in response['Messages']:
            msg = message['Body']
            msg = json.loads(msg)
            print(msg['Location'])
            slotNames = ["Location", "cuisine", "numOfPeople", "date", "time", "email"]
            loc = msg['Location']["value"]["interpretedValue"]
            cuisine = msg['cuisine']["value"]["interpretedValue"]
            date = msg['date']["value"]["interpretedValue"]
            time = msg['time']["value"]["interpretedValue"]
            email = msg['email']["value"]["interpretedValue"]
            numOfPeople = msg['numOfPeople']["value"]["interpretedValue"]
            restaurantIDs = getFromES(cuisine.lower())
            subj = f'Hello! Here are my {cuisine} restaurant suggestions for {numOfPeople} people, for {date} at {time} pm\n'
            # previousData = getDataFromDynamoEmail(email)
            for restaurantID in restaurantIDs:
                data = getDataFromDynamo(restaurantID)
                subj += data['name']['S'][2:-1] + ', located at ' + data['address']['S'] + '\n'
            # if previousData != "not found":
            #     subj += "We also have your previous recommendations \n"
                
            res = sendEmail(subj) 
            # Delete the processed message from the queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
    
    # TODO implement
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }