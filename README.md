# DJITelloPy
Based on [**Damià Fuentes Escoté**'s work](https://github.com/damiafuentes/TelloSDKPy).  
The initial version was extended with the possibility to detect objects in pseudo-real time (a few fps) with the camera.
Tested with Python 3.7, but it also may be compatabile with other versions.  

## Install through git clone
```
$ pip install --upgrade pip
$ git clone https://github.com/damiafuentes/TelloSDKPy.git
$ cd TelloSDKPy
$ pip install -r requirements.txt
```
Sometimes you need to update the virtual environment indexes and skeletons in order for the `example.py` file to work with `pygame`. If you are working with PyCharm, this can be done to ```File > Invalidate Caches```.  
You might want to [install opencv directly](https://www.pyimagesearch.com/opencv-tutorials-resources-guides/) instead of going through pip to improve speed. We did so on a mac book air from 2014 but it didn't seem to improve speed.  

## Usage
To simply show the output of the camera:
```
python main.py --option None
```
To perform object detection:
```
python main.py --option object_detection --model yolov3 --threshold .5 --nms .3 --input_size 320
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
