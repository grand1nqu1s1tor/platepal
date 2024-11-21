import json
import boto3
def lambda_handler(event, context):
    # TODO implement
    print(event)
    message = json.loads(event["body"])
    message = message["messages"][0]["unstructured"]["text"]
    # Send the user input to the Amazon Lex bot
    print(message)
    lex_runtime_v2 = boto3.client('lexv2-runtime')

    # Parameters for the RecognizeText API call
    params = {
        'botId': 'TITZO72HSE',
        'botAliasId': 'TSTALIASID',
        'localeId': 'en_US',
        'sessionId': 'uniqueSessionId',
        'text': message
    }
    newMessage = 'API under construction'
    try:
        # Send the message to Lex V2 bot
        response = lex_runtime_v2.recognize_text(**params)

        # Extract intent name and message
        intent_name = response['interpretations'][0]['intent']['name']
        newMessage = response['messages'][0]['content']
        print(intent_name)
    except Exception as e:
        print("Error:", e)
        return "Error occurred in Sending"
    print(response)
    
    return {
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'statusCode': 200,
        'body': json.dumps({
        'messages': [
          {
            'type': "unstructured",
            'unstructured': {
              'text': newMessage,
            },
          },
        ],
      },)
    }
