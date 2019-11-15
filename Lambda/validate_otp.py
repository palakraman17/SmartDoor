import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_passcodes = dynamodb.Table('passcodes')
table_visitors = dynamodb.Table('visitors')

def validate_otp(response_OTP):      #Validate otp from "passcodes" table
    if response_OTP is not None:
        #retr faceid
        responseData = table_visitors.query(KeyConditionExpression=Key('code').eq(response_OTP))
        if (responseData and len(responseData['Items']) >= 1 and responseData['Items'][0]):
            responseData = responseData['Items'][0]
            faceid = responseData['faceid']
                  
        #retrieve visitor name 
        name = visitor_info(faceid)
        print("Hi,"+name+ "Welcome!")
    else:
        print("Sorry! Owner didn't approve your access")
        
        
def visitor_info(faceid):    #Retrieve vistor information from "visitors" table
    responseData = table_visitors.query(KeyConditionExpression=Key('FaceId').eq(faceid))
    if (responseData and len(responseData['Items']) >= 1 and responseData['Items'][0]):
        responseData = responseData['Items'][0]
        name = responseData['Name']
    return name
    
    
def lambda_handler(event, context):
    response_OTP = event['code']
    #response_OTP = 4322
    validate_otp(response_OTP)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
