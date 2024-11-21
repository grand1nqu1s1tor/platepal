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
                        'Data': 'This is the message body in text format from the scheduler',
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
def getFromES(cuisineType):
    # es = Elasticsearch(
    #     hosts=[{'host': 'https://search-restaurant-jv5qmadw254con55bfymtebw7i.us-east-1.es.amazonaws.com', 'port': 443}],
    #     use_ssl=True,
    #     verify_certs=True,
    #     http_auth=('yelp-restaurants', 'Yelprestaurants!123')
    # )
    es_endpoint = 'https://search-restaurant-jv5qmadw254con55bfymtebw7i.us-east-1.es.amazonaws.com'
    index_name = 'restaurants'
    search_url = f"https://{es_endpoint}/{index_name}/_search"
    search_query = {
        "query": {
            "match": {
                "Cuisine": cuisineType
            }
        }
    }
    # Perform search
    try:
        # Perform search
        response = requests.get(search_url, json=search_query)

        # Process response
        if response.status_code == 200:
            search_results = response.json()
            return search_results
        else:
            return {"statusCode": response.status_code, "body": response.text}

    except requests.exceptions.RequestException as e:
        return {"statusCode": 500, "body": str(e)}
def lambda_handler(event, context):
    getFromES("italian")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/211125538864/Q1'
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )
    
    # Check if messages are received
    if 'Messages' in response:
        for message in response['Messages']:
            # Process the message (e.g., execute business logic)
            sendEmail(message)
            
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

