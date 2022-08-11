import argparse
import random
import shutil
import os

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',type=str, default='')
    parser.add_argument('--output',type=str, default='')
    parser.add_argument('--idprefix',type=str, default='')
    parser.add_argument('--limit', type=int, default=0)
    return parser.parse_args()

def copy_files(source, output, idprefix, limit):
    label_dir = os.path.join(output,'Label')
    if not os.path.isdir(label_dir):
        os.mkdir(label_dir)

    # source files
    files = []
    for file in os.listdir(os.path.join(source,"Label")):
        filename, ext = os.path.splitext(file)
        files.append(filename)

    samples = range(0,len(files))
    if limit > 0:
        samples = random.sample(range(0,len(files)),limit)

    for id in samples:
        filename = files[id]
        img = os.path.join(source,filename+'.jpg')
        label = os.path.join(source,'Label',filename+'.txt')
        shutil.copy2(img, output)
        os.rename(os.path.join(output,filename+'.jpg'),os.path.join(output,idprefix+filename+'.jpg'))
        shutil.copy2(label,label_dir)
        os.rename(os.path.join(label_dir,filename+'.txt'),os.path.join(label_dir,idprefix+filename+'.txt'))

        print("copying {} file of {}".format(id+1,len(samples)))
    print("{} examples of {} were copied".format(len(samples),len(files)))
    return

if __name__ == '__main__':
    args = getArgs()
    source = args.source
    output = args.output
    idprefix = args.idprefix
    limit = args.limit

    # create output dir
    if not os.path.isdir(output):
        os.mkdir(output)

    copy_files(source, output, idprefix, limit)
