# Image Detection API - Kubernate Version



## Project Overview

This project aims at building a web-based system that allows end-users to send an image to a web service hosted in a Docker container and receive a list of objects detected in their uploaded image. The project makes use of YOLO (You only look once) library, a state-of-the-art real-time object detection system, and OpenCV (Open-Source Computer Vision Library) to perform required image operations/transformations. Both YOLO and OpenCV are python-based open-source computer vision and
machine learning software libraries. The web service will be hosted as container in a Kubernetes cluster.

Kubernetes is used as the container orchestration system. The object detection web service is also designed to be a RESTful API that can use Python's FLASK library. 

The performance of iWebLens by varying the rate of requests sent to the system (demand) and the number of existing Pods within the Kubernetes cluster (resources) are tested and the result can be seen in the excel file.



### Video Presentation

A video presentation can be seen in following URL:

https://youtu.be/fvJzbrOIxKo



### API Configuration

host address configured in code:

host : '0.0.0.0'

port : 5000

URI : /api/predict

Http Method : GET





## Contact

email: shain.jobseeking@gmail.com

wechat: zsy9266266

