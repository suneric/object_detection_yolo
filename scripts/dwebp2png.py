import glob, os
from PIL import Image
dir = "/home/ubuntu/Downloads/1"
for file in os.listdir(dir):
    imgFile = os.path.join(dir,file)
    img = Image.open(imgFile)
    if img.format == "WEBP":
        filename, ext = os.path.splitext(imgFile)
        print(filename+".jpg")
        img.save(filename+".jpg","jpeg")
