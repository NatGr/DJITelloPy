import cv2
import numpy as np
import time


class FrameProcessor():
    """class responsible for processing a video frame captured from the drone into a frame that can be displayed by
    pygames. This class itself doesn't do much but it will be inherited by a more specialized class"""
    def __init__(self):
        super(FrameProcessor, self).__init__()
        self.frame = np.zeros((3, 960, 720), dtype=np.uint8)
        self.out_frame = np.zeros((3, 960, 720), dtype=np.uint8)

    def process(self, frame):
        """simply converts the color and disposition of the frame"""
        self.frame = frame
        self.preprocess_frame()
        self.postprocess_frame()
        time.sleep(1 / 30)  # sleeps so that we have approx 30 fps

    def preprocess_frame(self):
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

    def postprocess_frame(self):
        self.frame = np.rot90(self.frame)
        self.out_frame = np.flipud(self.frame)
