import json
import numpy as np
import sys
import time
import cv2
import os
import boto3
import uuid
from urllib.parse import unquote_plus
import base64

s3_client = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'images'
confthres = 0.5
nmsthres = 0.1


def get_labels(labels_path):
    # load the COCO class labels our YOLO model was trained on
    # lpath=os.path.sep.join([yolo_path, labels_path])

    # print(yolo_path)
    labelFile = s3_client.get_object(Bucket="yoloconfig", Key=labels_path)
    LABELS = labelFile['Body'].read().decode('utf8').splitlines()
    # labelFile = s3_client.Object("yoloconfig", labels_path)
    # LABELS = open(labelFile).read().strip().split("\n")
    return LABELS


def get_weights(weights_path):
    # derive the paths to the YOLO weights and model configuration
    # weightsPath = os.path.sep.join([yolo_path, weights_path])
    weightsPath = s3_client.get_object(Bucket="yoloconfig", Key=weights_path)
    weightsFile = weightsPath['Body'].read()
    # weightsFile = s3_client.download_file("yoloconfig","yolov3-tiny.weights","/tmp")
    # with open('yolov3-tiny.weights', 'r') as f:
    #     weightsFile = s3.download_fileobj('yoloconfig', '/yolov3-tiny.weights', f)
    return weightsFile


def get_config(config_path):
    # configPath = os.path.sep.join([yolo_path, config_path])
    # configFile = s3_client.download_file("yoloconfig","yolov3-tiny.cfg","/tmp")
    configPath = s3_client.get_object(Bucket="yoloconfig", Key=config_path)
    configFile = configPath['Body'].read()
    # with open('yolov3-tiny.cfg', 'r') as f:
    #     configFile = s3.download_fileobj('yoloconfig', '/yolov3-tiny.cfg', f)
    return configFile


def load_model(configpath, weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)

    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net


def do_prediction(image, net, LABELS):
    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    # print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])

                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # TODO Prepare the output as required to the assignment specification
    # ensure at least one detection exists
    labels = []
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            print("detected item:{}, accuracy:{}, X:{}, Y:{}, width:{}, height:{}".format(LABELS[classIDs[i]],
                                                                                          confidences[i],
                                                                                          boxes[i][0],
                                                                                          boxes[i][1],
                                                                                          boxes[i][2],
                                                                                          boxes[i][3]))
            labels.append(LABELS[classIDs[i]])
    return labels


## Yolov3-tiny versrion
labelsPath = "coco.names"
cfgpath = "yolov3-tiny.cfg"
wpath = "yolov3-tiny.weights"


def lambda_handler(event, context):
    try:
        resMessage = "erro"
        base64Image = event['file']
        baseTemp = base64Image.split(",")
        base64Image = baseTemp[1]
        img = base64.b64decode(base64Image)
        img = bytearray(img)
        npimg = np.asarray(img, dtype="uint8")
        # npimg=np.array(img)
        image = npimg.copy()
        # image=cv2.cvtColor(np.float32(image),cv2.COLOR_BGR2RGB)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        Lables = get_labels(labelsPath)
        CFG = get_config(cfgpath)
        Weights = get_weights(wpath)
        # load the neural net.  Should be local to this method as its multi-threaded endpoint
        nets = load_model(CFG, Weights)
        # TODO: change return of do_prediction;

        labels = do_prediction(image, nets, Lables)
        lab = ""

        for i in labels:
            lab += i + ","
        if lab == "":
            lab = "NA"
            resMessage = ""
        else:
            lab = lab[:-1]
            client = boto3.resource("dynamodb")
            table = client.Table("images")
            image_list = table.scan()['Items']
            imgListMock = []
            image_dict = {}
            tag_list = lab.split(",")
            image_tag_list = []
            for record in image_list:
                if (set(tag_list).issubset(set(record['tags'].split(",")))):
                    image_tag_list = record['tags'].split(',')
                    image_dict = {
                        "url": record['url'],
                        "tags": image_tag_list
                    }
                imgListMock.append(image_dict)
            resMessage = imgListMock
    except Exception as e:
        print("Exception  {}".format(e))
    return resMessage
    # return {"statusCode": 200,"headers": {"content-type": "application/json"},"body": imgListMock}