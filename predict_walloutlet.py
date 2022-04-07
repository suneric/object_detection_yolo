import argparse
import numpy as np
import torch
import cv2

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',type=str, default='')
    parser.add_argument('--yolov5',type=str,default='trained/walloutlet.pt')
    return parser.parse_args()

def draw_prediction(img,box,valid,confidence,label):
    if valid:
        H,W = img.shape[:2]
        text_horizontal = 0
        l,t,r,b = int(box[0]),int(box[1]),int(box[2]),int(box[3])
        cv2.rectangle(img, (l,t), (r,b), (0,255,0), 2)
        cv2.putText(img, label, (l-10,t-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        texts = [
            ("confidence","{:.2f}".format(confidence))
        ]
        for (i,(k,v)) in enumerate(texts):
            text = "{}:{}".format(k,v)
            cv2.putText(img, text, (10+text_horizontal*100,H-((i*20)+20)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.imshow('walloutlet detection',img)
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

    yolov5 = args.yolov5
    model = torch.hub.load('ultralytics/yolov5','custom', path=yolov5)
    results = model(resized)
    labels, cord = results.xyxy[0][:, -1].cpu().numpy(), results.xyxy[0][:, :-1].cpu().numpy()
    print(labels, cord)

    draw_prediction(resized, cord[0][0:4], True, cord[0][4], "Type B")
    cv2.destroyAllWindows()
