# AWS-Docker-Kubernate

### Intro
This repository contains two projects:`Image Object Detection API` and `Online Image Storage System`.

The API provides users with a web service that can detect the objects in the image sent and return a json formated response to the user which list all detected objects. 

Further, a modern online image storage system is developed using AWS services, which gives users CRUD functions to manage images and automatically add tags to the image based on the objects detected in the image. The tag can be edited and also images can be found and returned according to the tag provided by user.

Specific introduction can be seen in the readme file in each projects.

### Techniques Involved
Image Object Detection API:
`Docker`, `Flask`, `Kubernates`, `YOLO`,` OpenCV`
Online Image Storage System:
AWS Services such as `S3`, `Lambda`, `DynamoDB`, `Layer`, `IAM`, `Trigger` etc
`YOLO`,` OpenCV`

### CAUTION
The `Online Image Storage System` is a group-developed project, the task allocation as the following:

@Shain (`author`): `Image Detection Lambda`,` S3 bucket configuration`, `find image by image Lambda`, `API configuration`, `Dynamo Database configuration`, `Layer creation`, `IAM configuration`  etc.

@Elvis Zewen Li: `Front end development`, `Authentication`, `IAM configuration` etc.

@Zih Jia Yeh: `Find image by tag`, `API configuration`, `IAM configuration`, `DynamoDB configuration`, `IAM configuratoin` etc.

@KeWu: Edit image tags, delete tags/images, API configuration, IAM configuration, `DynamoDB configuration`,`IAM configuration` etc.

