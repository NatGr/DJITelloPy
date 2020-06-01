# DJITelloPy
Based on [**Damià Fuentes Escoté**'s work](https://github.com/damiafuentes/TelloSDKPy).  
The initial version was extended with the possibility to detect objects or to perform key-point detection in real time with the camera.  
This might run on CPU or GPU (key-point detection only works on CPU).  
Tested with Python 3.7, but it also may be compatabile with other versions.  

## Install
```
pip install -r requirements.txt
```
If you want to use a GPU to perform inference, you will need to [install opencv directly](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/) instead of going through pip (opencv is installed through pip in requirements.txt).  
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
