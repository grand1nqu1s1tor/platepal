import json
import boto3
import uuid
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the boto3 Lex V2 client outside of the lambda_handler to utilize AWS Lambda's execution context reuse
client = boto3.client('lexv2-runtime', region_name='us-east-1')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/891377008581/UserPreferenceQueue.fifo'


# List of valid locations and cuisines for validation
valid_locations = ["new york", "manhattan", "nyc"]
valid_cuisines = ["indian", "thai", "american", "chinese", "italian", "mexican"]

def lambda_handler(event, context):
    # Log the received event for debugging purposes
    print("Received event: " + json.dumps(event))

    # Check the invocation source to determine the next action
    if event.get('invocationSource') == 'DialogCodeHook':
        # Perform necessary validation
        return handle_validation(event)
    elif event.get('invocationSource') == 'FulfillmentCodeHook':
        # Perform the fulfillment and return the appropriate response
        return handle_fulfillment(event)
    else:
        # Process a standard request coming from API Gateway or another source
        return handle_standard_request(event)

def handle_validation(event):
    # Extract slots from the event
    slots = event['sessionState']['intent']['slots']
    
    # Validate the 'Location' slot
    location_slot = slots.get('Location')
    if location_slot:
        location_value = location_slot.get('value', {}).get('interpretedValue').lower()
        
        # Check if the location is in the list of valid locations
        if location_value not in valid_locations:
            # If the location is not valid, elicit the 'Location' slot again with a message
            return elicit_slot(
                intent_name=event['sessionState']['intent']['name'],
                slots=slots,
                slot_to_elicit='Location',
                message_content=f"The location '{location_value}' is not valid. Please provide a valid location."
            )
    
    # If all validations pass, delegate back to Lex to continue
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'Delegate'
            },
            'intent': event['sessionState']['intent']
        }
    }


def handle_fulfillment(event):
    # Extract slots from the event
    print(json.dumps(event, indent=4))  # Debugging: Print the event structure
    slots = event['sessionState']['intent']['slots']

    # Initialize message attributes
    message_attributes = {}
    
    # Check required slots and prepare message attributes
    for slot_name in ['CuisineType', 'Location']:
        slot_value = slots.get(slot_name, {}).get('value', {}).get('interpretedValue')
        if slot_value:
            message_attributes[slot_name] = {
                'StringValue': slot_value,
                'DataType': 'String'
            }

    # Construct the message body with slot values
    message_body = json.dumps({
        slot_name: attributes['StringValue']
        for slot_name, attributes in message_attributes.items()
    })

    # Send the message to SQS
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body,
        MessageAttributes=message_attributes,
        MessageGroupId='UserPreference'  # Required for FIFO queues
    )

    print(f"Message sent to SQS with Message ID: {response['MessageId']}")

    # Prepare the Lex V2 response
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled'
            },
            'intent': {
                'name': event['sessionState']['intent']['name'],
                'state': 'Fulfilled'
            }
        },
        'messages': [{
            'contentType': 'PlainText',
            'content': 'Thank you, we are processing your request.'
        }]
    }


def handle_standard_request(event):
    #Troubleshooting
    logger.info("Received event: %s", json.dumps(event))
    # Extract the session ID from the request headers or generate a new one
    session_id = event['headers'].get('Session-Id', str(uuid.uuid4()))
    # Log the session ID
    logger.info("Session ID: %s", session_id)
    
    
    # Extract the last user message from the event
    try:
        body = json.loads(event.get('body', '{}'))
        lastUserMessage = body.get('messages')[0]['unstructured']['text']
    except (json.JSONDecodeError, IndexError, TypeError) as e:
        return {'statusCode': 400, 'body': json.dumps("Invalid request format")}
    
    # Check if a session ID was provided, if not generate a new one
    session_id = event['headers'].get('Session-Id')
    if not session_id:
        session_id = '123e4567-e89b-12d3-a456-426614174000' #str(uuid.uuid4())

    # Call Lex V2 recognize_text API
    response = client.recognize_text(
        botId="UY4NMMWKAS",
        botAliasId="2EOIQTWGMN",
        localeId="en_US",
        sessionId=session_id,
        text=lastUserMessage
    )
    
    # Process and return the Lex V2 response
    return handle_lex_response(response)

def handle_lex_response(response):
    # Extract the message from the Lex response
    botMessage = response.get('messages', [{}])[0].get('content', "I'm not sure how to respond to that.")
    
    # Return the message in the format expected by the API Gateway
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'messages': [{'type': 'unstructured', 'unstructured': {'text': botMessage}}]})
    }

def elicit_slot(intent_name, slots, slot_to_elicit, message_content):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit,
            },
            'intent': {
                'name': intent_name,
                'slots': slots,
                'state': 'InProgress'
            }
        },
        'messages': [{
            'contentType': 'PlainText',
            'content': message_content
        }]
    }

