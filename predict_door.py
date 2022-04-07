import argparse
import numpy as np
import torch
import cv2
import os
from math import ceil

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',type=str, default='')
    parser.add_argument('--yolov5',type=str,default='trained/doorhandle.weights')
    return parser.parse_args()

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def split_image(image):
    width = image.shape[1]
    height = image.shape[0]
    result = []
    if width > height:
        n_image = ceil(width/height*2)
        left = 0
        for i in range(int(n_image)):
            if left + height > width:
                left = width - height
            result.append((left, 0, height, height))
            left += int(height/2)
    else:
        n_image = ceil(height/width*2)
        top = 0
        for i in range(int(n_image)):
            if top + width > height:
                top = height - width
            result.append((0, top, width, width))
            top += int(width/2)
    return result

def detection_output(img, weights, config, classes):
    W = img.shape[1]
    H = img.shape[0]

    net = cv2.dnn.readNet(weights,config)

    scale = 0.00392 # 1/255
    blob = cv2.dnn.blobFromImage(img,scale,(416,416),(0,0,0),True,crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids=[]
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * W)
                center_y = int(detection[1] * H)
                w = int(detection[2] * W)
                h = int(detection[3] * H)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x,y,w,h])
    # crop square subimage and do further detection
    sub_img_list = split_image(img)
    for s in sub_img_list:
        sub_img = img[s[1]:s[1]+s[3], s[0]:s[0]+s[2]]
        blob = cv2.dnn.blobFromImage(sub_img, scale, (416,416), (0,0,0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(get_output_layers(net))
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * s[2]) + s[0]
                    center_y = int(detection[1] * s[3]) + s[1]
                    w = int(detection[2] * s[2])
                    h = int(detection[3] * s[3])
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    outputs = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        label = classes[class_ids[i]]
        confidence = confidences[i]
        outputs.append((class_ids[i], label, box, confidence))
    return outputs

def draw_prediction(img,targets,COLORS):
    H,W = img.shape[:2]
    text_horizontal = 0
    for item in targets:
        class_id = item[0]
        label = item[1]
        box = item[2]
        confidence = item[3]
        l,t,r,b = int(box[0]),int(box[1]),int(box[0]+box[2]),int(box[1]+box[3])
        cv2.rectangle(img, (l,t), (r,b), COLORS[class_id], 2)
        cv2.putText(img, label, (l-10,t-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[class_id], 2)
        texts = [
            ("confidence","{:.2f}".format(confidence))
        ]
        for (i,(k,v)) in enumerate(texts):
            text = "{}:{}".format(k,v)
            cv2.putText(img, text, (l-10,t-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[class_id], 2)

    cv2.imshow('door and handle',img)
    cv2.waitKey(10000)


if __name__ == "__main__":
    args = getArgs()
    image = args.image
    img = cv2.imread(image)
    scale_percent = 30 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    classes = []
    with open('trained/door.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    config = 'trained/yolo-door.cfg'
    outputs = detection_output(resized,args.yolov5,config,classes)
    print(outputs)
    COLORS = [(255,0,0),(0,255,0),(0,0,255)]
    draw_prediction(resized, outputs, COLORS)
    cv2.destroyAllWindows()
