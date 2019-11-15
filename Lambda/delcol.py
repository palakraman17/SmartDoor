import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    list_faces_in_collection('Collection')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



def delete_faces_from_collection(collection_id, faces):

    client=boto3.client('rekognition')

    response=client.delete_faces(CollectionId=collection_id,
                               FaceIds=faces)
    
    print(str(len(response['DeletedFaces'])) + ' faces deleted:') 							
    for faceId in response['DeletedFaces']:
         print (faceId)
    return len(response['DeletedFaces'])

def list_faces_in_collection(collection_id):


    maxResults=2
    faces_count=0
    tokens=True

    client=boto3.client('rekognition')
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)

    print('Faces in collection ' + collection_id)
    dele=[]
 
    while tokens:

        faces=response['Faces']
        
        for face in faces:
            print (face)
            dele.append(face['FaceId'])
            
            faces_count+=1
        delete_faces_from_collection('Collection',dele)
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False
    return faces_count   
