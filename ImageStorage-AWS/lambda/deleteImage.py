import json
import boto3


def lambda_handler(event, context):
    client = boto3.resource("dynamodb")
    table = client.Table("images")
    image_list = table.scan()['Items']
    image_dict = {}
    url = event['url']
    id = -1
    for image in image_list:
        if(image['url']==url):
            id = image['id']
            image_url = url
            image_tags = image['tags']
    if(id!=-1):
        image_dict={
            "url": image_url,
            "tags": image_tags
        }
        response = table.delete_item(
                        Key={
                            'id': id
                        }
                    )  
        return image_dict            
    return "no record"