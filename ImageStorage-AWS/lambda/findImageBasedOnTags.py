import json
import boto3

def lambda_handler(event, context):
    client = boto3.resource("dynamodb")
    print(event)
    table = client.Table("images")
    image_list = table.scan()['Items']
    imgListMock=[]
    image_dict = {}
    if event['key1']=='all':
        for record in image_list:
            image_tag_list=record['tags'].split(',')
            image_dict={
                    "url": record['url'],
                    "tags": image_tag_list
                }
            imgListMock.append(image_dict)
    else:
        tag_list = event['key1'].split(",")
        image_tag_list = []
        for record in image_list:
            if(set(tag_list).issubset(set(record['tags'].split(",")))):
                image_tag_list=record['tags'].split(',')
                image_dict={
                    "url": record['url'],
                    "tags": image_tag_list
                }
                imgListMock.append(image_dict)

    return imgListMock
    #return {"statusCode": 200,"headers": {"content-type": "application/json"},"body": imgListMock}