# Downloading models

### MaskRCNN
[Download the weights](http://download.tensorflow.org/models/object_detection/mask_rcnn_inception_v2_coco_2018_01_28.tar.gz). Then extract frozen_graph.pb and move it in "models/maskrcnn/model.pb".

### MiDasv2
You can download the onnx model [here](https://github.com/intel-isl/MiDaS/tree/master/tf#make-onnx-model-from-downloaded-pytorch-model-file) and put the file in "midas/model.onnx".  
As midas is trained to provide a scale and shift invariant prediction, it is not supposed to be used to estimate absolute depth here.

### Yolov4 320
In order to use a yolov4 model for object detection, you must download
a YOLOv4 model trained on COCO trainval [here](https://github.com/AlexeyAB/darknet#pre-trained-models) and save it as "models/yolov4/model.weights".  

### YOLOv3 320

In order to use a yolov3 model for object detection, you must download
a YOLOv3-320 model trained on COCO trainval [here](https://pjreddie.com/darknet/yolo/) and save it as "models/yolov3/model.weights".  

### YOLOv3 tiny

[Download the weights](https://pjreddie.com/darknet/yolo/) in "models/yolov3_tiny/model.weights".  

### SSD-Mobilenetv1
[Donwload the weights](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz). Then extract frozen_graph.pb and move it in "models/ssd_mobv1/model.pb".  

### SSD-Mobilenetv2
[Donwload the weights](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz). Then extract frozen_graph.pb and move it in "models/ssd_mobv2/model.pb".  

### PoseNet
[Download the tflite file](https://www.tensorflow.org/lite/models/pose_estimation/overview)

### Openpose
From the models directory do
```
wget -c http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/coco/pose_iter_440000.caffemodel -O openpose/model.caffeemodel
```
(these instructions come from [here](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/models/getModels.sh)).  
Openpose was however never integrated since PoseNet already does the job. If you are interested in multi persumns keypoint evaluation, openpose is the way to go.  
