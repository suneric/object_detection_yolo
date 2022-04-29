import cv2
import pandas as pd
import glob
import os
import random
import argparse

"""
export your labels to YOLO format, with one *.txt file per image
(if no objects in image, no *.txt file is required).
The *.txt file specifications are:
- One row per object
- Each row is class x_center y_center width height format.
- Box coordinates must be in normalized xywh format (from 0 - 1).
- Class numbers are zero-indexed (start from 0).
"""

def oid2yolo(source, dest, class_index):
    img_dest = creatSubFolder(dest,'images')
    label_dest = creatSubFolder(dest,'labels')
    copyImageAndLabel(source,'train', class_index, img_dest, label_dest)
    copyImageAndLabel(source,'validation', class_index, img_dest, label_dest)
    copyImageAndLabel(source,'test', class_index, img_dest, label_dest)


def copyImageAndLabel(source, category ,class_index, img_dest, label_dest):
    # create destination directories
    img_output = creatSubFolder(img_dest,category)
    label_output = creatSubFolder(label_dest,category)

    img_dir = os.path.join(source,category)
    label_dir = os.path.join(source, category, 'Label')
    for file in os.listdir(label_dir):
        filename,ext = os.path.splitext(file)
        img_file = os.path.join(img_dir,filename+'.jpg')
        label_file = os.path.join(label_dir,file)
        convertAnnotation(filename, img_file,label_file,class_index,img_output,label_output)


def convertAnnotation(filename, img_file, label_file, class_index, img_dest, label_dest):
    annotation = []
    with open(label_file,'r') as f:
        for line in f.read().splitlines():
            data = line.split(' ')
            left = float(data[len(data)-4])
            top = float(data[len(data)-3])
            right = float(data[len(data)-2])
            bottom = float(data[len(data)-1])
            idx = class_index.index(data[0])
            annotation.append((idx,left,top,right,bottom))

    img = cv2.imread(img_file)
    H,W,C = img.shape
    img_output = os.path.join(img_dest,filename+'.jpg')
    cv2.imwrite(img_output,img)

    label_output = os.path.join(label_dest,filename+'.txt')
    with open(label_output,'w') as f:
        for item in annotation:
            # print(item)
            # resize the box to [0,1]
            x_center = 0.5*(item[1]+item[3])/W
            y_center = 0.5*(item[2]+item[4])/H
            width = (item[3]-item[1])/W
            height = (item[4]-item[2])/H
            f.write(str(item[0])+' '+str(x_center)+' '+str(y_center)+' '+str(width)+' '+str(height)+'\n')
    return

def creatSubFolder(root,sub):
    dest = os.path.join(root,sub)
    if not os.path.isdir(dest):
        os.mkdir(dest)
        print("create folder of {0}".format(dest))
    return dest


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',type=str, default='')
    parser.add_argument('--output',type=str, default='')
    return parser.parse_args()

if __name__ == '__main__':
    args = getArgs()
    dest = args.output
    source = args.source
    class_index = ['outerBox','typeB']
    oid2yolo(source, dest, class_index)
