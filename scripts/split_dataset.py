import os, sys
import argparse
import random
import shutil

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',type=str, default=None,help="root path of source")
    parser.add_argument('--output',type=str, default=None,help="the output root path")
    return parser.parse_args()

def dataset_summary(image,label):
    class_instances = [0,0,0,0,0,0] # 0,1,2,3,4 five classes + 5 background
    file_list = [set(),set(),set(),set()]
    for file in os.listdir(image):
        if os.path.isdir(os.path.join(image,file)):
            continue
        img_file = os.path.join(image,file)
        filename, ext = os.path.splitext(file)
        label_file = os.path.join(label,filename+'.txt')
        if not os.path.exists(label_file):
            file_list[0].add(file)
            class_instances[-1] += 1
        else:
            with open(label_file,'r') as f:
                for line in f.read().splitlines():
                    data = line.split(' ')
                    class_id = int(data[0])
                    class_instances[class_id] += 1
                    if class_id == 0 or class_id == 1:
                        file_list[1].add(file)
                    elif class_id == 2:
                        file_list[2].add(file)
                    elif class_id == 3 or class_id == 4:
                        file_list[3].add(file)
                    else:
                        print("unexpected class id")
    return (class_instances, file_list)

def copy_file(image_list, src_dir, image_dir, label_dir = None):
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)
    for image in image_list:
        img_file = os.path.join(src_dir,'images',image)
        shutil.copy2(img_file, image_dir)

    if label_dir is None:
        return

    if not os.path.exists(label_dir):
        os.mkdir(label_dir)
    for file in image_list:
        filename,ext = os.path.splitext(file)
        label_file = os.path.join(src_dir,'labels',filename+'.txt')
        shutil.copy2(label_file, label_dir)


if __name__ == '__main__':
    args = get_args()
    image_src = os.path.join(args.source,'images')
    label_src = os.path.join(args.source,'labels')
    info = dataset_summary(image_src, label_src)
    print("instance", info[0])
    print("file count", len(info[1][0]), len(info[1][1]), len(info[1][2]), len(info[1][3]))
    # split to dataset to train, validate, test
    if args.output is not None:
        if not os.path.exists(args.output):
            os.mkdir(args.output)
        image_dir = os.path.join(args.output,'images')
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        label_dir = os.path.join(args.output,'labels')
        if not os.path.exists(label_dir):
            os.mkdir(label_dir)

        print("copy background images...")
        background_list = list(info[1][0])
        copy_file(background_list,args.source,os.path.join(image_dir,'train'))

        print("copy class 0 and 1 images...")
        class_1_list = list(info[1][1])
        random.shuffle(class_1_list)
        split_1 = int(0.9*len(class_1_list))
        copy_file(class_1_list[:split_1],args.source,os.path.join(image_dir,'train'), os.path.join(label_dir,'train'))
        copy_file(class_1_list[split_1:],args.source,os.path.join(image_dir,'test'), os.path.join(label_dir,'test'))

        print("copy class 2 images...")
        class_2_list = list(info[1][2])
        random.shuffle(class_2_list)
        split_2 = int(0.9*len(class_2_list))
        copy_file(class_2_list[:split_2],args.source,os.path.join(image_dir,'train'), os.path.join(label_dir,'train'))
        copy_file(class_2_list[split_2:],args.source,os.path.join(image_dir,'test'), os.path.join(label_dir,'test'))

        print("copy class 3 and 4 images...")
        class_3_list = list(info[1][3])
        random.shuffle(class_3_list)
        split_3 = int(0.9*len(class_3_list))
        copy_file(class_3_list[:split_3],args.source,os.path.join(image_dir,'train'), os.path.join(label_dir,'train'))
        copy_file(class_3_list[split_3:],args.source,os.path.join(image_dir,'test'), os.path.join(label_dir,'test'))

        train_info = dataset_summary(os.path.join(image_dir,'train'), os.path.join(label_dir,'train'))
        print("instance in train", train_info[0])
        test_info = dataset_summary(os.path.join(image_dir,'test'), os.path.join(label_dir,'test'))
        print("instance in test", test_info[0])
