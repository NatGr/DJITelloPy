# DJITelloPy
Based on [**Damià Fuentes Escoté**'s work](https://github.com/damiafuentes/TelloSDKPy).  
The initial version was extended with the possibility to detect objects, to perform key-point detection or depth estimation in real time with the camera.  
This might run on CPU or GPU (key-point detection only works on CPU).  
Tested with Python 3.7 and 3.6, but it also may be compatabile with other versions.  

## Performances
in frames per second:

|  | Yolov4 320 | Yolov3 320 | Yolov3 tiny 416 | ssd_mobv2 300 | ssd_mobv1 300 | posenet 257 | MaskRCNN 320 | Midas 384 |   
| -------- | ------- | ---------- | ----------- | --------- | --------- | ------- |   ------- |   ------- |    
| mac book air 2014 | ? | ~1 | ~4 | ~3.5 | ~4 | ~4 | ~0.2 | ? |    
| Intel i5-4670 | ~2 | ~2 | ~10 | ~5 | ~6 | ~4 | ~0.5 | ~0.5 |   
| NVIDIA GTX 970 | ~9 | ~7 | ~11 | ~4 | ~5 | - |   ~3   |   ~4  |    

* the i5 and the gtx 970 are hardware that costed around 200 euros each in 2016. These were part of a desktop "gaming" computer.
* For object detection models, FPS vary depending on what is on screen, we show average cases. This seems to be due to the significant time required to draw all of the boxes in an image (up to 0.1s, a good portion of it being spent in other threads -- A solution would be to reimplement everything in C++).
* GPU is necessary for bigger networks and does not really bring speed improvements for smaller ones
* There are nets with unknown perfs on the macbook air because 


## Install
```
pip install -r requirements.txt
```
If you want to use a GPU to perform inference, you will need to [install opencv directly](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/) instead of going through pip (opencv is installed through pip in requirements.txt).  
Yolov4 and Midas requires opencv version at least 4.4.  
You need to download models before usning them, see models/README.md on that.

### Compile OpenCV on ubuntu:
The tutorial is very well made but does not [include cuda support](https://gist.github.com/YashasSamaga/985071dc57885348bec072b4dc23824f). To compile with that you should change the cmake command to:
```
cmake -D CMAKE_BUILD_TYPE=RELEASE \                                                                                                                                                 
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_CUDA=ON \
    -D WITH_CUDNN=ON \
    -D OPENCV_DNN_CUDA=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=/home/nathan/opencv_contrib/modules \
    -D PYTHON_EXECUTABLE=/home/nathan/miniconda3/bin/python3.7 \
    -D PYTHON_PACKAGES_PATH=/home/nathan/miniconda3/lib/python3.7/site-packages \
    -D PYTHON_LIBRARY=/home/nathan/miniconda3/lib/libpython3.7m.so \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D BUILD_EXAMPLES=OFF ..
```
I let my paths to give an idea of their locations, these are to change of course (and don't use "~" instead of "/home/use", it fucks everything up).   
Additionnally, when using CPU only, compiling opencv is around 30% faster on the gaming pc, while I saw no differnece on the macbook.  


Installing tf-lite (for posenet) is also necessary, see [this page](https://www.tensorflow.org/lite/guide/python).  

### Compile OpenCV on windows (you should use Ubuntu if you can):
[This ressource](https://jamesbowley.co.uk/accelerating-opencv-4-build-with-cuda-intel-mkl-tbb-and-python-bindings/) and [that one](https://www.learnopencv.com/install-opencv3-on-windows) helped me a lot. I faced several bugs during installation, in the end, what worked for me was to (with CUDA, cudnn and intel MKL; [I had to use python 3.6, it did not work with 3.7](https://github.com/opencv/opencv/issues/16449)):

1. Use Microsoft Visual Studio 14.0 (the year of the version is 2015)
2. In CMake GUI:
    1. use x64 as generator
    2. Set the following flags *before* clicking on configure the first time:
        - WITH_CUDA ON
        - WITH_CUDNN ON
        - OPENCV_DNN_CUDA ON
        - OPENCV_EXTRA_MODULES_PATH YOUR_PATH/opencv_contrib-4.4.0/modules
        - OPENCV_ENABLE_NONFREE ON
        - MKLROOT C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl
        - MKL_INCLUDE_DIRS C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/include
        - MKL_ROOT_DIR C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl
        - PYTHON3_INCLUDE_DIR C:/Users/Nathan/miniconda3/include
        - PYTHON3_LIBRARY C:/Users/Nathan/miniconda3/libs/python36.lib
        - BUILD_opencv_python3 ON

## Usage
To simply show the output of the camera:
```
python main.py --option None
```
To perform object detection:
```
python main.py --option object_detection --model yolov3 --threshold .5 --nms .3 --input_size 320  --use_gpu
```
To see the different options:
```
python main.py -h
```
The controls are:
- T: Takeoff
- L: Land
- Arrow keys: Forward, backward, left and right.
- A (Q if --azerty flag is set) and D: Counter clockwise and clockwise rotations
- W (Z if --azerty flag is set) and S: Up and down.

### Notes
- If you are using the ```streamon``` command and the response is ```Unknown command``` means you have to update the Tello firmware. That can be done through the Tello app.
- Mission pad detection and navigation is only supported by the Tello EDU.
- Connecting to an existing wifi network is only supported by the Tello EDU.
- When connected to an existing wifi network video streaming is not available.
