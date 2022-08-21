import json
import cv2
import pandas as pd
import glob
import os
import random
import shortuuid
import argparse


def get_labels(annotation_file, type='vgg'):
    labels = []
    with open(annotation_file) as f:
        if type == 'vgg':
            jdata = json.load(f)
            imgIds = jdata["_via_image_id_list"]
            for id in imgIds:
                img = jdata["_via_img_metadata"][id]
                filename = img["filename"]
                record = []
                record.append(filename)
                boxes = []
                box = img["regions"][0]["shape_attributes"]
                label = img["regions"][0]["region_attributes"]["Outlet Type"]
                boxes.append((label, box["x"],box["y"],box["x"]+box["width"],box["y"]+box["height"]))
                record.append(boxes)

                labels.append(record)
        elif type == 'agi': # argumented images
            jdata = json.load(f)
            for id in jdata:
                item = jdata[id]
                box = item["shape_attributes"]
                filename = id
                label = "Wall Outlet"
                labels.append((filename, label, box["x"],box["y"],box["x"]+box["width"],box["y"]+box["height"]))
    return labels

"""
convert vgg annotation format to oid format
https://github.com/EscVM/OIDv4_ToolKit

separate all image into three categories: train (75%), validation (15%), test (10%)
one label file (.txt) for each image file, annotation like:
"classname left top right bottom"

"""
def vgg2oid(img_path, annotation_file, output_root, id_prefix, type):
    # import json
    labels = get_labels(annotation_file)
    print("find {} images".format(len(labels)))
    if len(labels) == 0:
        return

    # split to train 80%, validation 10%, test 10%
    random.shuffle(labels)
    count1 = round(0.80*len(labels))
    count2 = round(0.10*len(labels))
    train = labels[0:count1]
    validation = labels[count1:count1+count2]
    test = labels[count1+count2:]
    # print(len(train)+len(validation)+len(test))

    # create destination folder
    train_dir = os.path.join(output_root,'train')
    if not os.path.isdir(train_dir):
        os.mkdir(train_dir)
    for item in train:
        copyImageAndLabel(img_path,item,id_prefix,train_dir)

    val_dir = os.path.join(output_root,'validation')
    if not os.path.isdir(val_dir):
        os.mkdir(val_dir)
    for item in validation:
        copyImageAndLabel(img_path,item,id_prefix,val_dir)

    test_dir = os.path.join(output_root,'test')
    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)
    for item in test:
        copyImageAndLabel(img_path,item,id_prefix,test_dir)


def copyImageAndLabel(image_path,label,id_prefix,destination):
    # make a folder for Label
    label_folder = os.path.join(destination,'Label')
    if not os.path.isdir(label_folder):
        os.mkdir(label_folder)
    # load image
    origin_img = cv2.imread(os.path.join(image_path,label[0]))
    # create unique filename for image and label
    filename = id_prefix+'-'+shortuuid.uuid()
    img_name = filename + '.jpg'
    label_name = filename + '.txt'
    # copy image
    cv2.imwrite(os.path.join(destination,img_name),origin_img)
    with open(os.path.join(label_folder,label_name),'w') as f:
        for box in label[1]:
            class_name = box[0]
            lx,ty,rx,by = box[1],box[2],box[3],box[4]
            f.write(class_name+' '+str(lx)+' '+str(ty)+' '+str(rx)+' '+str(by)+'\n')


"""
this is for process new label file containing multiple boxes
"""
def get_labels_2(annotation_file, img_path):
    labels = []
    with open(annotation_file) as f:
        jdata = json.load(f)
        for item in jdata:
            # check if file is exists
            filename = jdata[item]['filename']
            if not os.path.exists(os.path.join(img_path, filename)):
                print(filename, "does not exist")
                continue

            record = []
            record.append(filename)
            regions = jdata[item]['regions']
            boxes = []
            for r in regions:
                box = r['shape_attributes']
                label = r['region_attributes']['outlet']
                boxes.append((label, box["x"], box["y"], box["x"]+box["width"], box["y"]+box["height"]))
            record.append(boxes)
            labels.append(record)
    return labels

def convertVGG2OID(img_path, annotation_file, output_root, id_prefix):
    # import json
    labels = get_labels_2(annotation_file,img_path)
    print("find {} images".format(len(labels)))
    if len(labels) == 0:
        return

    # split to train 80%, validation 10%, test 10%
    random.shuffle(labels)
    count1 = round(0.80*len(labels))
    count2 = round(0.10*len(labels))
    train = labels[0:count1]
    validation = labels[count1:count1+count2]
    test = labels[count1+count2:]
    # print(len(train)+len(validation)+len(test))

    # create destination folder
    train_dir = os.path.join(output_root,'train')
    if not os.path.isdir(train_dir):
        os.mkdir(train_dir)
    for item in train:
        copyImageAndLabel(img_path,item,id_prefix,train_dir)

    val_dir = os.path.join(output_root,'validation')
    if not os.path.isdir(val_dir):
        os.mkdir(val_dir)
    for item in validation:
        copyImageAndLabel(img_path,item,id_prefix,val_dir)

    test_dir = os.path.join(output_root,'test')
    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)
    for item in test:
        copyImageAndLabel(img_path,item,id_prefix,test_dir)




def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',type=str, default='./origin/self-captured/images')
    parser.add_argument('--label',type=str, default='./origin/self-captured/labels/8.10.2 Outlet ID.json')
    parser.add_argument('--id_prefix',type=str, default='sc')
    parser.add_argument('--output', type=str, default='./output')
    parser.add_argument('--type', type=str, default='vgg')
    return parser.parse_args()

"""
suppose all the vgg images are in one folder (--image), and the annotation json file (--label) in another folder.
give a prefix for unique id (--id_prefix) and folder of output oid dataset (--output)
the dataset will be split to train (80%), validation(10%), and test (10%) sets
with one annotation file for each image. The annotation files (.txt) are in the folder 'Label' of each class.
"""
if __name__ == '__main__':
    args = getArgs()
    image_path = args.image
    annotations = args.label
    id_prefix = args.id_prefix
    output_root = args.output
    type = args.type

    if not os.path.isdir(output_root):
        os.mkdir(output_root)

    # vgg2oid(image_path,annotations,output_root,id_prefix, type)
    convertVGG2OID(image_path,annotations,output_root,id_prefix)
