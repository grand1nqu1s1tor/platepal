import json
import boto3
def validateSlots(slots):
    slotNames = ["Location", "cuisine", "numOfPeople", "date", "time", "email"]
    for name in slotNames:
        if name == 'Location' and slots[name] != None:
          if slots[name]["value"]["interpretedValue"].lower() not in ["new york", "manhattan", "nyc"]:
            slots[name] = None
            return name, "We only support Manhattan please try again"
        if name == 'cuisine' and slots[name] != None:
          if slots[name]["value"]["interpretedValue"].lower() not in ["indian", "italian", "chinese"]:
            slots[name] = None
            return name, "We only support indian, italian, chinese please try again"
        if name == 'numOfPeople' and slots[name] != None:
          if int(slots[name]["value"]["interpretedValue"]) > 20:
            slots[name] = None
            return name, "We only support upto 20 people"
        if slots[name] == None:
            return (name, "")
    return "completed", ""
def sendQueue(message):
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/211125538864/Q1'
    
    # Replace 'YOUR_MESSAGE_BODY' with the message body you want to send
    message_body = 'Hello from Lambda!'
    
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )
    
    # Log message ID for confirmation
    print("Message sent successfully:", response['MessageId'])
    
    # Return response
    return {
          "sessionState": {
            "dialogAction": {
              "type": "ElicitIntent"
            },
            
          },
          "messages": [
            {
              "contentType": "PlainText",
              "content": " You’re all set. Expect my suggestions shortly! Have a good day",
              
            },
          ]
        }
def lambda_handler(event, context):
    print(event)    
    # TODO implement
    intent = event["interpretations"][0]["intent"]
    intentName = intent['name']
    
    if intentName == 'GreetingIntent':
        print('here')
        return {
          "sessionState": {
            "dialogAction": {
              "type": "ElicitIntent"
            },
            
          },
          "messages": [
            {
              "contentType": "PlainText",
              "content": "How can I help you?",
              
            },
          ]
        }
    elif intentName == 'recommendRestaurants':
        slots = intent['slots']
        slot, messageBySlot = validateSlots(slots)
        if messageBySlot == "":
          if slot == 'completed':
            res = sendQueue(slots)
            return res
          return {
            "sessionState": {
              "dialogAction": {
              "slotToElicit": slot,
                "type": "ElicitSlot"
              },
              "intent": {
              "name": intentName,
              "slots": slots,
              }
              
            }
          }
        else:
          return {
            "sessionState": {
              "dialogAction": {
              "slotToElicit": slot,
                "type": "ElicitSlot"
              },
              "intent": {
              "name": intentName,
              "slots": slots,
              }
              
            },
            "messages": [
            {
            "contentType": "PlainText",
            "content": messageBySlot,
            }
          ]
          }
          
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
