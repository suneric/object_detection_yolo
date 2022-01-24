import tensorflow as tf
import argparse
from PIL import Image
import numpy as np
import torch

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',type=str, default='')
    parser.add_argument('--yolov5',type=str,default='')
    return parser.parse_args()

def load(imagefile):
    newImg = None
    width,height=0,0
    with Image.open(imagefile) as img:
        width, height = img.size
        newImg = img.resize((640,640))
        newImg = np.expand_dims(newImg, axis=0)
    return newImg,width,height

if __name__ == "__main__":
    args = getArgs()
    image = args.image
    yolov5 = args.yolov5

    model = torch.hub.load('ultralytics/yolov5', yolov5)
    img2predict,width,height = load(image)
    results = model(img2predict)
    labels, cord = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
    print(labels, cord)
