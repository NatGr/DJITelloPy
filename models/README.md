# Downloading models

## YOLOv3 320  

In order to use a yolov3 model for object detection, you must download
a YOLOv3-320 model trained on COCO trainval [here](https://pjreddie.com/darknet/yolo/) and save it as "models/yolov3_320/model.weights".  

## YOLOv3 tiny

[Download the weights](https://pjreddie.com/darknet/yolo/) in "models/yolov3_tiny/model.weights".  

## SSD-Mobilenetv1
[Donwload the weights](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz). Then extract frozen graph.pb and move it in models/ssd_mobv1/model.pb  

## SSD-Mobilenetv2
[Donwload the weights](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz). Then extract frozen graph.pb and move it in models/ssd_mobv2/model.pb  

## PoseNet
[Download the tflite file](https://www.tensorflow.org/lite/models/pose_estimation/overview) 

#### (Openpause) As inference takes 4 seconds on a mac book air, the code was not configured to use openpose
From the models directory do
```
wget -c http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/coco/pose_iter_440000.caffemodel -O openpose/model.caffeemodel
```
(these instructions come from [here](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/models/getModels.sh))