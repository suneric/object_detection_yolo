# object_detection_yolo
An object detection experiment using yolov5

# Object Detection Challenge

## Prerequisite
- [Operation System: Ubuntu 18.04](./doc/ubuntu_installation.md)
- [Nvidia GPU support](./doc/nvidia_gpu_support.md)
- [Package Manager: Anaconda](./doc/anaconda_installation.md)

## create a GPU environment
tensorflow 2.1.0 is the last version to support python 2
```
conda env create -f py3-tf2-gpu.yml
conda activiate py3-tf2-gpu
```
my nvidia card is RTX3070, requires nvidia driver version > 450, so cudatoolkit version should >= 11.0
using cudatoolkit 10 may cause compatibility issues for gpu support when using tensorflow.
- the above conda environment will install python 3.7 and cudatoolkit 11.0.
- install tensorflow 2.4.0 separately, don't install it with conda as it will install cuda 10.2 and cudnn 7 along side, so it may conflict with the new version installed.
```
pip install tensorflow-gpu
```
- download [cudnn 8](https://developer.nvidia.com/rdp/cudnn-download#a-collapse805-110), and copy all the files from bin folder of the downloaded, cudnn 8 folder, then paste it in the bin folder of the conda environment folder.
```
tar -xzvf cudnn-11.0-linux-x64-v8.0.5.39.tgz

# copy and past to conda envs lib and include
sudo cp cuda/include/cudnn*.h   /anaconda3/envs/py3-tf2-gpu/include
sudo cp cuda/lib64/libcudnn*    /anaconda3/envs/py3-tf2-gpu/lib
sudo chmod a+r /usr/local/cuda/include/cudnn*.h    /anaconda3/envs/py3-tf2-gpu/lib/libcudnn*

```

## Open Image Data v6 Download
1. clone the code
```
git clone https://github.com/pythonlessons/OIDv4_ToolKit.git
```
2. download class "Apple"
```
python main.py downloader --classes Apple --type_csv validation
```
An OID folder will be created with two sub folder "csv_folder" and "Dataset" where all the downloaded images are located. Ignore the promot "Error", Enter "y" for download the missing file
3. support OIDv6 download
  - open https://storage.googleapis.com/openimages/web/download.html, click "V6" button in the first line and then scroll down to "Download the annotations and metadata" and click "Train" button to download train csv file in "Boxes" row.
  - After downloading, put the "oidv6-train-annotations-bbox.csv" into the folder of "OID/scv_folder", and change the name to "train-annotation-bbox.csv" (you also can edit the code in main.py if you don't want to rename the csv file)
  - repeat previous steps for downloading the "test" and "validation" annotation bbox
  - now the csv_folder contains 4 files including the "class-description-boxable.csv"
  - use the same command as usual.
4. download images
  - create classes.txt (specify your interested classes)
  - download all the images of interested classes with a limited number for train, validation and test
  ```
  python main.py downloader --classes classes.txt --type_csv train --limit 1500
  ```

## Play with yolov5
1. clone the code
```
git clone https://github.com/ultralytics/yolov5.git
```
2. Prepare data [tips](https://github.com/ultralytics/yolov5/wiki/Tips-for-Best-Training-Results), visualize annotation using script **visualize_annotation**
```
python visualize_annotation.py --image [OID images] --label [OID image labels] --type [oid|vgg]
```
3. convert oid dataset to yolov5 data set using script **annotation_oid2yolo**
```
python annotation_oid2yolo.py --source [OID images] --output [Yolo format output] --class_index [index of specified class defined in dataset.yaml]
```
4. trainwith yolov5
```
python train.py --data dataset.yaml --weights yolov5s --batch 16 --img 640 --epochs 300          
```


## References
- [OIDv4 Toolkit](https://github.com/pythonlessons/OIDv4_ToolKit.git)
- [OIDv4-tfrecord generator](https://github.com/zamblauskas/oidv4-toolkit-tfrecord-generator)
- [Train Custom Data with yolov5](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data)
