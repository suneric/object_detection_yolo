import argparse
import numpy as np
import torch

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',type=str, default='')
    parser.add_argument('--yolov5',type=str,default='yolov5/runs/train/exp/weigths/best.pt')
    return parser.parse_args()

if __name__ == "__main__":
    args = getArgs()
    image = args.image
    yolov5 = args.yolov5
    model = torch.hub.load('ultralytics/yolov5','custom', path=yolov5)
    results = model(image)
    labels, cord = results.xyxy[0][:, -1], results.xyxy[0][:, :-1]
    print(labels, cord)
    results.show()
