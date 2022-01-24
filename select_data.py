import argparse
import random
import shutil
import os

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',type=str, default='')
    parser.add_argument('--output',type=str, default='')
    parser.add_argument('--limit', type=int, default=0)
    return parser.parse_args()

def copy_files(source, output, category, count):
    # output directory
    output_dir = os.path.join(output,category)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    label_dir = os.path.join(output_dir,'Label')
    if not os.path.isdir(label_dir):
        os.mkdir(label_dir)

    # source files
    files = []
    for file in os.listdir(os.path.join(source,category)):
        filename, ext = os.path.splitext(file)
        files.append(filename)

    samples = random.sample(range(0,len(files)),count)
    for id in samples:
        filename = files[id]
        img = os.path.join(source,category,filename+'.jpg')
        label = os.path.join(source,category,'Label',filename+'.txt')
        shutil.copy2(img, output_dir)
        shutil.copy2(label,label_dir)
    print("copy {} examples of {}".format(count,len(files)))
    return

if __name__ == '__main__':
    args = getArgs()
    source = args.source
    output = args.output
    limit = args.limit

    if not os.path.isdir(output):
        os.mkdir(output)

    train_count = int(limit*0.8)
    val_count = int(limit*0.1)
    test_count = int(limit*0.1)

    copy_files(source, output, 'train', train_count)
    copy_files(source, output, 'validation', val_count)
    copy_files(source, output, 'test', test_count)
