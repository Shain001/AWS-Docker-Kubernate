'''
 @author : Shenyi Zhang
 @student_id: 30359953

 This program is based on the code provided by the teaching team of FIT5225 Monash University
 The webservice function is append to the modified original code provided.
 
 ALl the path-related function in the linux environment is changed, the original file in windows is not changed
'''
# import the necessary packages
import base64

from PIL import Image

import numpy as np
import sys
import time
import cv2
from io import BytesIO
import io
from flask import Flask, request, Response, jsonify
import json
import os

# construct the argument parse and parse the arguments
confthres = 0.3
nmsthres = 0.1

def get_labels(labels_path):
    # load the COCO class labels our YOLO model was trained on
    lpath=os.path.sep.join([yolo_path, labels_path])

    print("yolopath: " + yolo_path)
    print("lpath: " + lpath)
    # LABELS = open(lpath).read().strip().split("\n")
    LABELS = open(labels_path).read().strip().split("\n")
    return LABELS


def get_weights(weights_path):
    # derive the paths to the YOLO weights and model configuration
    # weightsPath = os.path.sep.join([yolo_path, weights_path])
    weightsPath = weights_path
    return weightsPath

def get_config(config_path):
    # configPath = os.path.sep.join([yolo_path, config_path])
    configPath = config_path
    return configPath

def load_model(configpath,weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net

def do_prediction(image,net,LABELS):

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
    #print(layerOutputs)
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
    # ensure at least one detection exists、
    json_obj = {'id': 0, 'object': []}
    temp_dict = {'label': 0, 'accuracy': 0, 'rectangle': {'height': 0, 'left': 0, 'top': 0, 'width': 254}}
    if len(idxs) > 0:
        # build the dictionary first and then dynamically update it inside the loop
        # json_obj is the final dictionary that will be converted to the json object
        # temp_dict is the dictionary for each object, if more than one object exists, just append the temp_dict to
        # the json_obj['object']

        # loop over the indexes we are keeping
        for i in idxs.flatten():
            print("detected item:{}, accuracy:{}, X:{}, Y:{}, width:{}, height:{}".format(LABELS[classIDs[i]],
                                                                                             confidences[i],
                                                                                             boxes[i][0],
                                                                                             boxes[i][1],
                                                                                             boxes[i][2],
                                                                                               boxes[i][3]))
            # update the object temp dictionary and append it to the json_obj dictionary
            temp_dict['label'] = LABELS[classIDs[i]]
            temp_dict['accuracy'] = confidences[i]
            temp_dict['rectangle']['width'] = boxes[i][2]
            temp_dict['rectangle']['height'] = boxes[i][3]
            temp_dict['rectangle']['left'] = boxes[i][0]
            temp_dict['rectangle']['top'] = boxes[i][1]
            json_obj['object'].append(temp_dict)

    return json_obj



## argument
#if len(sys.argv) != 3:
    #raise ValueError("Argument list is wrong. Please use the following format:  {} {} {}".
                     #format("python iWebLens_server.py", "<yolo_config_folder>", "<Image file path>"))

#yolo_path  = str(sys.argv[1])
#mark
yolo_path = ''
## Yolov3-tiny versrion
labelsPath= "coco.names"
cfgpath= "yolov3-tiny.cfg"
wpath= "yolov3-tiny.weights"

Lables=get_labels(labelsPath)
CFG=get_config(cfgpath)
Weights=get_weights(wpath)


#TODO, you should  make this console script into webservice using Flask

app = Flask(__name__)


@app.route('/api/predict', methods=['POST'])
def main():
    try:
        # imagefile = str(sys.argv[2])

        # grab data from the request body first
        data = request.json
        # transform the format to dictionary
        data = json.loads(data)
        img = data['image']
        id = data['id']
        # img = img.encode('utf-8')
        # img = base64.b64decode(img)
        #img = Image.open(io.BytesIO(img))

        # convert the format of the images from string to bytes
        img = base64.b64decode(img)
        img = Image.open(io.BytesIO(img))
        npimg = np.array(img)
        image = npimg.copy()

        # adjust the color and then do the prediction
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # load the neural net.  Should be local to this method as its multi-threaded endpoint
        nets = load_model(CFG, Weights)
        json_obj = do_prediction(image, nets, Lables)

        # here inside the returned dictionary, the id has not been assigned, therefore we assign the recieved id to it
        json_obj['id'] = id

        # convert to json format
        json_obj_converted = json.dumps(json_obj)
        return Response(response= json_obj_converted, status=200, mimetype='application/json')

    except Exception as e:

        print("Exception  {}".format(e))


@app.route('/test', methods=['POST','GET'])
def test():
    print('working')
    return'working'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


