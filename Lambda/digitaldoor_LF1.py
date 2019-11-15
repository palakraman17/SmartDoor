import json
import math,random
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    #photoname = event['Records'][0]['s3']['object']['key']
    #add_faces_to_collection('buckethw2','KQF1W2xCO.jpg','Collection')
    detect('KQF1W2xCO.jpg')
  #  SendOTP(2);
    #if(event.Records[0].s3.object.size>0):
     #   detect(photoname)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def SendOTP(faceid):
    string = '0123456789'
    OTP = "" 
    length = len(string) 
    for i in range(4) : 
        OTP += string[math.floor(random.random() * length)] 
  
    print(OTP)
    
    #logger.info("Inside sendMailToUser")
    #RECIPIENT = requestData['Phone']['StringValue']
    #logger.info(RECIPIENT)
    AWS_REGION = 'us-east-1'      
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('visitors')
    faceid=str(faceid)
    responseData = table.query(KeyConditionExpression=Key('FaceId').eq(faceid))
    print(responseData)
    
    if (responseData and len(responseData['Items']) >= 1 and responseData['Items'][0]):

        responseData = responseData['Items'][0]
        phone = responseData['Phone']
        client = boto3.client('sns',region_name=AWS_REGION)
    
   # try:
        
        response = client.publish(
            PhoneNumber = phone,
            Message="Your OTP is " + OTP
            )
        
        table = dynamodb.Table('passcodes')
        table.put_item(
        Item={
        'FaceId': faceid,
        'code': int(OTP),
        'expiry' : int(time.time() + 300)
    }
    )


def detect(photoname):
    AWS_REGION = 'us-east-1'
    dynamodb = boto3.resource('dynamodb')
    bucket='buckethw2'
    collectionId='Collection'
    #photoname='frame.jpg'
    threshold = 70
    maxFaces=2

    client=boto3.client('rekognition')

  
    response=client.search_faces_by_image(CollectionId=collectionId,
                                Image={'S3Object':{'Bucket':bucket,'Name':photoname}},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)
    
    faceMatches=response['FaceMatches']
    print ('Matching faces')
    if len(faceMatches)>0:
        for match in faceMatches:
                print ('FaceId:' + match['Face']['FaceId'])
                faceid=match['Face']['FaceId']
                #print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
                print
        SendOTP(faceid)
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        timestamp=str(timestamp)
        table = dynamodb.Table('visitors')
        response = table.update_item(
        Key={
        'FaceId': faceid,
        },
        UpdateExpression = 'SET photos = list_append(photos, :newitem)',
        ExpressionAttributeValues={
            ":newitem": [
                    {
                    'objectKey': photoname,
                    'bucket': 'buckethw2',
                    'createdTimestamp': timestamp    
                    }
            ]
        },
        #ReturnValues="UPDATED_NEW"
    )
        
        
    else:
        print("No face match")
        client = boto3.client('sns',region_name=AWS_REGION)
    
    #try:
        response = client.publish(
            PhoneNumber = "+19293404302",
            Message="You have a new guest. Please authenticate him/her using the link below. https://buckethw2.s3.amazonaws.com/wpi.html"
        )
        table = dynamodb.Table('visitors')
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        timestamp=str(timestamp)
        faceid=add_faces_to_collection('buckethw2',photoname,'Collection')
        table.put_item(
        Item={
        'FaceId': faceid,
        'Name': 'YTBS',
        #'expiry' : int(time.time() + 300)
        'Phone': 'YTBS',
        'photos': [
            {
            'objectKey': photoname,
            'bucket': 'buckethw2',
            'createdTimestamp':
            timestamp
            }
            ]
        }
        )
       # SendOTP(faceid)
   

def add_faces_to_collection(bucket,photo,collection_id):

    client=boto3.client('rekognition')

    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo) 	
    print('Faces indexed:')						
    for faceRecord in response['FaceRecords']:
        print('  Face ID: ' + faceRecord['Face']['FaceId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
        faceid=faceRecord['Face']['FaceId']
    '''
    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])
    '''
    return faceid
        
    
 
    