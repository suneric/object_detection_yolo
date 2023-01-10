import json
import cv2
import pandas as pd
import glob
import os,sys
import random
import shortuuid
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import shutil

"""
convert vgg annotation to yolo format
"""

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',type=str, default=None,help="the path of images")
    parser.add_argument('--label',type=str, default=None,help="the path of annotation JSON file")
    parser.add_argument('--output',type=str, default=None,help="the output root path")
    return parser.parse_args()

def show_image_and_annotation(image, annotation):
    # draw annotations
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 50)
    colors = ["#6495ED","#DE3163", "red", "#FFBF00", "#9FE2BF"]
    classes = ['door','door handle','human body','electric wall outlet','type b socket hole']
    with Image.open(image) as img:
        w,h = img.size
        scale = int(w/100)
        if h < w:
            scale = int(h/100)
        draw = ImageDraw.Draw(img)
        for (classname,left,top,right,bottom) in annotation:
            print(classname)
            color = colors[classes.index(classname)]
            draw.rectangle(((round(left),round(top)),(round(right),round(bottom))),outline=color, width=scale)
            draw.text((round(left)+10,round(top)+20), classname, font=fnt, fill=color)
    return img

"""
resize image
"""
def resize_image(image, width, height):
    origin_width, origin_height = image.size
    if origin_width <= width and origin_height <= height:
        return image
    scale_w = width / origin_width
    scale_h = height / origin_height
    if scale_w > scale_h:
        return image.resize((int(origin_width*scale_h), int(height)))
    else:
        return image.resize((int(width),int(origin_height*scale_w)))

"""
Display images in a directory
"""
class ImageDisplay(tk.Frame):
    def __init__(self, parent, image, label, output):
        self.root = parent
        self.root.bind('<Left>',self.left_pressed)
        self.root.bind('<Right>',self.right_pressed)
        self.find_images_and_labels(image, label)
        self.max_count = len(self.images)-1
        self.counter = 0
        self.create_canvas()
        self.create_output_yolo(output)

    def left_pressed(self,event):
        self.prev_image()

    def right_pressed(self,event):
        self.next_image()

    def create_output_yolo(self, output):
        self.output = output
        if not os.path.exists(self.output):
            os.mkdir(self.output)
            print("Directory {} is created".format(self.output))

        imgFolder = os.path.join(output,'images')
        if not os.path.exists(imgFolder):
            os.mkdir(imgFolder)
            print("Directory {} is created".format(imgFolder))

        labelFolder = os.path.join(output,'labels')
        if not os.path.exists(labelFolder):
            os.mkdir(labelFolder)
            print("Directory {} is created".format(labelFolder))

        tempFolder = os.path.join(output,'unqualify')
        if not os.path.exists(tempFolder):
            os.mkdir(tempFolder)
            print("Directory {} is created".format(tempFolder))

    def create_canvas(self):
        self.root.title("Image Annotation Visualizer")
        self.root.config(bg='#4a7a8c')
        self.frame_btn = tk.Frame(self.root,relief=tk.RAISED,height=5)
        self.frame_btn.pack()
        self.frame_cv = tk.Frame(self.root,relief=tk.FLAT,height=640)
        self.frame_cv.pack()
        button_n = tk.Button(self.frame_btn, text='Prev', height=2, width=8, command=self.prev_image)
        button_n.pack(side=tk.LEFT)
        button_p = tk.Button(self.frame_btn, text='Next', height=2, width=8, command=self.next_image)
        button_p.pack(side=tk.LEFT)
        button_q = tk.Button(self.frame_btn, text='yolo', height=2, width=8, bg='yellow', command=self.move_to_yolo)
        button_q.pack(side=tk.LEFT)
        button_u = tk.Button(self.frame_btn, text='unqualify', height=2, width=8, bg='red', command=self.move_to_unqualify)
        button_u.pack(side=tk.LEFT)
        button_lr = tk.Button(self.frame_btn, text='rotate left', height=2, width=8, bg='blue', command=self.rotate_left)
        button_lr.pack(side=tk.LEFT)
        button_rr = tk.Button(self.frame_btn, text='rotate right', height=2, width=8, bg='blue', command=self.rotate_right)
        button_rr.pack(side=tk.LEFT)
        button_d = tk.Button(self.frame_btn, text="Delete", height=2, width=8, bg='yellow', command=self.delete_image)
        button_d.pack(side=tk.LEFT)
        self.canvas = tk.Canvas(self.frame_cv, width=640, height=640, bg='white')
        self.canvas.pack(padx=2,pady=2)
        self.canvas_image = self.get_image(0)
        self.photo = self.canvas.create_image(0,0,anchor='nw',image=self.canvas_image)
        imgFile = self.images[0]
        filename, ext = os.path.splitext(os.path.basename(imgFile))
        self.count_str = "This is the first image of {}: {}".format(self.max_count+1, filename)
        self.count_label = tk.Label(self.frame_cv, text=self.count_str)
        self.count_label.pack()

    def get_image(self,count):
        imgFile = self.images[count]
        basename = os.path.basename(imgFile)
        annotation = []
        if basename in self.labels.keys():
            annotation = self.labels[basename]
        print(basename, annotation)
        img = show_image_and_annotation(imgFile,annotation)
        img = resize_image(img,640,640)
        photo = ImageTk.PhotoImage(img)
        return photo

    def parse_label_3(self, imageDir, labelFile):
        self.labels = {}
        with open(labelFile) as f:
            jdata = json.load(f)
            imgIds = jdata["_via_image_id_list"]
            for id in imgIds:
                img = jdata["_via_img_metadata"][id]
                filename = img["filename"]
                if not os.path.exists(os.path.join(imageDir, filename)):
                    print(filename, "does not exist")
                    continue
                regions = img['regions']
                boxes = []
                for r in regions:
                    box = r['shape_attributes']
                    label = 'missing'
                    if len(r['region_attributes']) > 0:
                        label = r['region_attributes']['class'].lower()
                    boxes.append((label,box["x"],box["y"],box["x"]+box["width"],box["y"]+box["height"]))
                self.labels[filename] = boxes
            print("find {} labels".format(len(self.labels)))

    # olatz
    def parse_label_2(self, imageDir, labelFile):
        self.labels = {}
        with open(labelFile) as f:
            jdata = json.load(f)
            for id in jdata:
                img = jdata[id]
                filename = img["filename"]
                if not os.path.exists(os.path.join(imageDir, filename)):
                    print(filename, "does not exist")
                    continue
                regions = img['regions']
                boxes = []
                for r in regions:
                    box = r['shape_attributes']
                    label = 'missing'
                    if len(r['region_attributes']) > 0:
                        label = r['region_attributes']['class'].lower()
                        if 'electric wall' in label:
                            label = 'electric wall outlet'
                    boxes.append((label,box["x"],box["y"],box["x"]+box["width"],box["y"]+box["height"]))
                self.labels[filename] = boxes
            print("find {} labels".format(len(self.labels)))

    def parse_label(self, imageDir, labelFile):
        self.labels = {}
        with open(labelFile) as f:
            jdata = json.load(f)
            imgIds = jdata["_via_image_id_list"]
            for id in imgIds:
                img = jdata["_via_img_metadata"][id]
                filename = img["filename"]
                if not os.path.exists(os.path.join(imageDir, filename)):
                    print(filename, "does not exist")
                    continue
                regions = img['regions']
                boxes = []
                for r in regions:
                    box = r['shape_attributes']
                    label = 'missing'
                    if len(r['region_attributes']) > 0:
                        label = r['region_attributes']['Class'].lower()
                    boxes.append((label,box["x"],box["y"],box["x"]+box["width"],box["y"]+box["height"]))
                self.labels[filename] = boxes
            print("find {} labels".format(len(self.labels)))


    def find_images_and_labels(self, imageDir, labelFile):
        # find image
        self.images = []
        for file in os.listdir(imageDir):
            if os.path.isdir(os.path.join(imageDir,file)):
                continue
            else:
                imgFile = os.path.join(imageDir,file)
                self.images.append(imgFile)
        print("find {} images".format(len(self.images)))
        #self.parse_label(imageDir, labelFile)
        self.parse_label_2(imageDir, labelFile)
        #self.parse_label_3(imageDir, labelFile)


    def next_image(self):
        self.counter += 1
        if self.counter > self.max_count:
            self.counter = self.max_count
            imgFile = self.images[self.counter]
            filename, ext = os.path.splitext(os.path.basename(imgFile))
            self.count_str = "This is the last image of {}: {}".format(self.max_count+1, filename)
        else:
            imgFile = self.images[self.counter]
            filename, ext = os.path.splitext(os.path.basename(imgFile))
            self.count_str = "This is the {}th of {} image: {}".format(self.counter+1,self.max_count+1, filename)
            self.canvas_image = self.get_image(self.counter)
            self.canvas.itemconfig(self.photo,image=self.canvas_image)
        self.count_label.configure(text=self.count_str)

    def prev_image(self):
        self.counter -= 1
        if self.counter < 0:
            self.counter = 0
            imgFile = self.images[self.counter]
            filename, ext = os.path.splitext(os.path.basename(imgFile))
            self.count_str = "This is the first image of {}: {}".format(self.max_count+1, filename)
        else:
            imgFile = self.images[self.counter]
            filename, ext = os.path.splitext(os.path.basename(imgFile))
            self.count_str = "This is the {}th of {} image: {}".format(self.counter+1,self.max_count+1, filename)
            self.canvas_image = self.get_image(self.counter)
            self.canvas.itemconfig(self.photo,image=self.canvas_image)
        self.count_label.configure(text=self.count_str)

    def move_to_yolo(self):
        imgFile = self.images[self.counter]
        basename = os.path.basename(imgFile)
        annotation = []
        if basename in self.labels.keys():
            annotation = self.labels[basename]
        print(basename, annotation)
        # copy image file to "images" folder
        imgDst = os.path.join(self.output,'images',basename)
        shutil.copy2(imgFile,imgDst)
        print("copy image {} to yolo".format(imgDst))
        if len(annotation) > 0:
            classIndex = ['door','door handle','human body','electric wall outlet','type b socket hole']
            img = cv2.imread(imgDst)
            H,W,C = img.shape
            filename,ext = os.path.splitext(basename)
            labelDst = os.path.join(self.output,'labels',filename+'.txt')
            with open(labelDst,'w') as f:
                for item in annotation:
                    idx = classIndex.index(item[0])
                    xc = 0.5*(item[1]+item[3])/W
                    yc = 0.5*(item[2]+item[4])/H
                    width = (item[3]-item[1])/W
                    height = (item[4]-item[2])/H
                    f.write(str(idx)+' '+str(xc)+' '+str(yc)+' '+str(width)+' '+str(height)+'\n')
            print("copy label {} to yolo".format(labelDst))
        self.next_image()
        return

    def move_to_unqualify(self):
        imgFile = self.images[self.counter]
        basename = os.path.basename(imgFile)
        imgDst = os.path.join(self.output,'unqualify',basename)
        shutil.copy2(imgFile,imgDst)
        print("unqualify image {}".format(imgDst))
        self.next_image()
        return

    def rotate_left(self):
        imgFile = self.images[self.counter]
        with Image.open(imgFile) as img:
            img = img.rotate(90,expand=True)
            img.save(imgFile)
        self.canvas_image = self.get_image(self.counter)
        self.canvas.itemconfig(self.photo,image=self.canvas_image)

    def rotate_right(self):
        imgFile = self.images[self.counter]
        with Image.open(imgFile) as img:
            img = img.rotate(-90,expand=True)
            img.save(imgFile)
        self.canvas_image = self.get_image(self.counter)
        self.canvas.itemconfig(self.photo,image=self.canvas_image)

    def delete_image(self):
        imgFile = self.images.pop(self.counter)
        if os.path.exists(imgFile):
            os.remove(imgFile)
            print("delete image {}".format(imgFile))
        self.max_count -= 1
        self.counter -= 1
        self.next_image()



if __name__ == '__main__':
    args = get_args()
    if not args.image or not args.label or not args.output:
        print("invalid arguments, use --help")
    else:
        root = tk.Tk()
        myapp = ImageDisplay(root, args.image, args.label, args.output)
        root.mainloop()
