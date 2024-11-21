import requests

def lambda_handler(event, context):
    # Elasticsearch endpoint
    es_endpoint = 'https://search-restaurant-jv5qmadw254con55bfymtebw7i.us-east-1.es.amazonaws.com'

    # Elasticsearch index and document type
    index = 'restaurants'

    # Elasticsearch query
    query = {
        "size": 1,
        "query": {
            "function_score": {
                "query": {"match": {"Cuisine": "indian"}},
                "random_score": {}
            }
        }
    }

    # Authentication credentials
    auth = ('yelp-restaurants', 'Yelprestaurants!123')

    # Make request to Elasticsearch
    response = requests.post(f'{es_endpoint}/{index}/_search',
                             json=query,
                             auth=auth)

    # Handle response
    if response.status_code == 200:
        es_data = response.json()
        # Process Elasticsearch response data
        return es_data
    else:
        # Handle error
        return {
            'statusCode': response.status_code,
            'body': response.text
        }
print(lambda_handler(None, None))
# print(len(lambda_handler(None, None)['hits']))