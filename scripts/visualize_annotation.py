import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import argparse

def show_image_and_annotation(image, label, type):
    # parser annotations in label file
    annotation = []
    with open(label,'r') as f:
        for line in f.read().splitlines():
            data = line.split(' ')
            # class name
            class_name = data[0]
            # for the case that there are space in the name
            for i in range(1,len(data)-5):
                class_name +='-'
                class_name += data[i]

            if type == 'oid':
                # box positions
                left = float(data[len(data)-4])
                top = float(data[len(data)-3])
                right = float(data[len(data)-2])
                bottom = float(data[len(data)-1])
                annotation.append((class_name,left,top,right,bottom))
            elif type == 'yolo':
                cx = float(data[len(data)-4])
                cy = float(data[len(data)-3])
                width = float(data[len(data)-2])
                height = float(data[len(data)-1])
                annotation.append((class_name,cx,cy,width,height))

    # draw annotations
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 50)
    with Image.open(image) as img:
        draw = ImageDraw.Draw(img)
        if type == 'oid':
            for (classname,left,top,right,bottom) in annotation:
                draw.rectangle(((round(left),round(top)),(round(right),round(bottom))),outline="blue", width=3)
                draw.text((round(left)+10,round(top)-50), classname, font=fnt, fill="blue")
        elif type == 'yolo':
            width, height = img.size
            for (classname,cx,cy,bw,bh) in annotation:
                left = int((cx-0.5*bw)*width)
                top = int((cy-0.5*bh)*height)
                right = int((cx+0.5*bw)*width)
                bottom = int((cy+0.5*bh)*height)
                draw.rectangle(((round(left),round(top)),(round(right),round(bottom))),outline="blue", width=3)
                draw.text((round(left)+10,round(top)-50), classname, font=fnt, fill="blue")
    return img

def find_images(image, label):
    images = []
    for file in os.listdir(image):
        if os.path.isdir(os.path.join(image,file)):
            continue
        else:
            img_file = os.path.join(image,file)
            filename,ext = os.path.splitext(file)
            label_file = os.path.join(label,filename+'.txt')
            images.append((img_file,label_file))
    print("find {} images".format(len(images)))
    return images

def resize_image(image, width, height):
    origin_width, origin_height = image.size
    scale_w = width / origin_width
    scale_h = height / origin_height

    if scale_w > scale_h:
        return image.resize((int(origin_width*scale_h), int(height)))
    else:
        return image.resize((int(width),int(origin_height*scale_w)))

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image',type=str, default='')
    parser.add_argument('--label',type=str, default='')
    parser.add_argument('--type',type=str, default='oid')
    return parser.parse_args()


class ImageDisplay(tk.Frame):
    def __init__(self, parent, image, label, type):
        self.root = parent
        self.find_images(image, label)
        self.type = type
        self.max_count = len(self.images)-1
        self.counter = 0
        self.create_canvas()

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
        button_d = tk.Button(self.frame_btn, text="Delete", height=2, width=8, bg='yellow', command=self.delete_image)
        button_d.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.frame_cv, width=640, height=640, bg='white')
        self.canvas.pack(padx=2,pady=2)
        self.canvas_image = self.get_image(0)
        self.photo = self.canvas.create_image(0,0,anchor='nw',image=self.canvas_image)

        (img_file,label_file) = self.images[0]
        filename, ext = os.path.splitext(os.path.basename(img_file))
        self.count_str = "This is the first image of {}: {}".format(self.max_count+1, filename)
        self.count_label = tk.Label(self.frame_cv, text=self.count_str)
        self.count_label.pack()

    def get_image(self,count):
        (img_file, label_file) = self.images[count]
        print(count, img_file)
        img = show_image_and_annotation(img_file, label_file, self.type)
        img = resize_image(img,640,640)
        photo = ImageTk.PhotoImage(img)
        return photo

    """
    get all image files and label files under the folder
    """
    def find_images(self, image, label):
        self.images = []
        for file in os.listdir(image):
            if os.path.isdir(os.path.join(image,file)):
                continue
            else:
                img_file = os.path.join(image,file)
                filename,ext = os.path.splitext(file)
                label_file = os.path.join(label,filename+'.txt')
                self.images.append((img_file,label_file))
        print("find {} images".format(len(self.images)))
        return self.images

    def next_image(self):
        self.counter += 1
        if self.counter > self.max_count:
            self.counter = self.max_count
            (img_file,label_file) = self.images[self.counter]
            filename, ext = os.path.splitext(os.path.basename(img_file))
            self.count_str = "This is the last image of {}: {}".format(self.max_count+1, filename)
        else:
            (img_file,label_file) = self.images[self.counter]
            filename, ext = os.path.splitext(os.path.basename(img_file))
            self.count_str = "This is the {}th of {} image: {}".format(self.counter+1,self.max_count+1, filename)
            self.canvas_image = self.get_image(self.counter)
            self.canvas.itemconfig(self.photo,image=self.canvas_image)
        self.count_label.configure(text=self.count_str)

    def prev_image(self):
        self.counter -= 1
        if self.counter < 0:
            self.counter = 0
            (img_file,label_file) = self.images[self.counter]
            filename, ext = os.path.splitext(os.path.basename(img_file))
            self.count_str = "This is the first image of {}: {}".format(self.max_count+1, filename)
        else:
            (img_file,label_file) = self.images[self.counter]
            filename, ext = os.path.splitext(os.path.basename(img_file))
            self.count_str = "This is the {}th of {} image: {}".format(self.counter+1,self.max_count+1, filename)
            self.canvas_image = self.get_image(self.counter)
            self.canvas.itemconfig(self.photo,image=self.canvas_image)
        self.count_label.configure(text=self.count_str)

    def delete_image(self):
        (img_file, label_file) = self.images.pop(self.counter)
        if os.path.exists(img_file):
            os.remove(img_file)
        if os.path.exists(label_file):
            os.remove(label_file)
        self.max_count -= 1
        self.counter -= 1
        self.next_image()

if __name__ == '__main__':
    args = getArgs()
    image = args.image
    label = args.label
    type = args.type
    # assume that the image is a folder containing all the images need to be visualized
    # the lable is also a folder containing the corresponding label file with same name
    if os.path.isdir(image):
        root = tk.Tk()
        myapp = ImageDisplay(root, image, label, type)
        root.mainloop()
    else:
        img = show_image_and_annotation(image,label,type)
        img.show("Image Annotation Visualizer")

    # root = tk.Tk()
    # images = find_images(image,label)
    # (img_file, label_file) = images[0]
    # img = show_image_and_annotation(img_file,label_file)
    # img = resize_image(img,640,640)
    # img = ImageTk.PhotoImage(img)
    # tk.Label(root,image=img).pack()
    # root.mainloop()
