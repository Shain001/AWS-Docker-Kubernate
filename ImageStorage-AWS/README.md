# Online Image Storage System

## Project Overview
This project aims at building a clouded online system that allows users to store the images and retrieve the images based on the auto-generated tags. The focus of this project is to design a serverless application that allows the client to upload their images to public cloud storage.

Upon the image upload, the application automatically tags the image with the type of objects detected in it, for example, person,car, etc.

Later on, clients can query images based on the type of objects in the images. To this end, the
application provides users with a list of URLs for images that include specific queried objects.

Finally, the user can also implement edit tag functions to the images.

**CAUTION!  This is a group-developed project, task allocation as the following:**
@Shain (`author`): `Image Detection Lambda`,` S3 bucket configuration`, `find image by image Lambda`, `API configuration`, `Dynamo Database configuration`, `Layer creation`, `IAM configuration`  etc.
@Elvis Zewen Li: `Front end development`, `Authentication`, `IAM configuration` etc.
@Zih Jia Yeh: `Find image by tag`, `API configuration`, `IAM configuration`, `DynamoDB configuration`, `IAM configuratoin` etc.
@KeWu: Edit image tags, delete tags/images, API configuration, IAM configuration, `DynamoDB configuration`,`IAM configuration` etc.

## Techniques Involved:
Image Process:
`OpenCV`, `YOLO`
AWS:
`S3`, `Lambda`, `DynamoDB`, `Layer`, `IAM`, `Trigger` etc

## Prerequisites of Running the Project
`npm` `Vue3`
## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

