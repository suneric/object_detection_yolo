## Convert OID image to tfrecord
1. using the generator in "oid_tfrecord" or clone the original code, and make replace 'app' with 'compat.v1' in the code
```
git clone https://github.com/zamblauskas/oidv4-toolkit-tfrecord-generator.git
```
2. convert oid image dataset to tfrecord for train, validation and test
```
python generate-tfrecord.py \
--classes_file ../OIDv4_ToolKit/classes.txt \
--class_descriptions_file ../OIDv4_ToolKit/OID/csv_folder/class-descriptions-boxable.csv \
--annotations_file ../OIDv4_ToolKit/OID/csv_folder/train-annotations-bbox.csv \
--images_dir ../OIDv4_ToolKit/OID/Dataset/train \
--output_file ../dataset/oid/train.tfrecord \
```

## Yolov3-tensorflow2
1. clone the code
```
git clone https://github.com/zzh8829/yolov3-tf2.git
```
2. Convert yolo3 pre-trained Darknet weights
```
wget https://pjreddie.com/media/files/yolov3.weights -O data/yolov3.weights
python convert.py --weights ./data/yolov3.weights --output ./checkpoints/yolov3.tf
```
3. Verify model
```
python detect.py --image ./data/meme.jpg
```
## Training with your own interested classes
- with Transfer Learning
Origanl pretrained yolov3 has 80 classes, here we learn 9 classes.
```
python train.py \
	--dataset ../dataset/oid/train.tfrecord \
	--val_dataset ../dataset/oid/val.tfrecord \
	--classes ../OIDv4_ToolKit/classes.txt \
	--num_classes 9 \
	--mode fit --transfer darknet \
	--batch_size 16 \
	--epochs 10 \
	--weights ./checkpoints/yolov3.tf \
	--weights_num_classes 80 \
```
- Training from random weights
Training from scrath is very difficult to converge. The original paper trained darknet on imagenet before training the whole network as well.
```
python train.py \
	--dataset ./dataset/oid/train.tfrecord \
	--val_dataset ./dataset/oid/val.tfrecord \
	--classes ./OIDv4_ToolKit/classes.txt \
	--num_classes 9 \
	--mode fit --transfer none \
	--batch_size 16 \
	--epochs 10 \
```

## Inference
- detect from images
```
python detect.py \
	--classes ../OIDv4_ToolKit/classes.txt \
	--num_classes 9 \
	--weights ./checkpoints/yolov3_train_10.tf \
	--image ./data/street.jpg \
```
  - lower the threshold to recheck the result if it is not success in the first time.
  ```
  # in the model.py
  flags.DEFINE_float('yolo_iou_threshold', 0.5, 'iou threshold')
  flags.DEFINE_float('yolo_score_threshold', 0.5, 'score threshold')
  ```

- detect from validation set
```
python detect.py \
	--classes ../OIDv4_ToolKit/classes.txt \
	--num_classes 9 \
	--weights ./checkpoints/yolov3_train_10.tf \
	--tfrecord ./data/oidv6_val.tfrecord \
```

## References
- [Train YOLOv3 with OpenImagesv4](https://github.com/WyattAutomation/Train-YOLOv3-with-OpenImagesV4)
- [yolo3-tf2](https://github.com/zzh8829/yolov3-tf2.git)
