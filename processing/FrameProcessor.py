import cv2
import numpy as np
import time


class FrameProcessor():
    """class responsible for processing a video frame captured from the drone into a frame that can be displayed by
    pygames. This class itself doesn't do much but it will be inherited by a more specialized class"""
    def __init__(self):
        super(FrameProcessor, self).__init__()
        self.frame = np.zeros((3, 960, 720), dtype=np.uint8)  # frame is transposed during postprocessing for pygame
        self.out_frame = np.zeros((3, 960, 720), dtype=np.uint8)  # out_frame is transposed during postprocessing for
        # pygame
        self.fps = 0
        self.margin = 5  # space between the top of label and the top of the screen

    def process(self, frame: np.array, battery: int):
        """simply converts the color and disposition of the frame. We add battery info to the frame"""
        self.frame = frame
        self.preprocess_frame()
        time.sleep(1 / 30)  # sleeps so that we have approx 30 fps
        self.postprocess_frame(battery)

    def preprocess_frame(self):
        self.start = time.time()
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

    def postprocess_frame(self, battery: int):
        """adds infos about fps and battery to the image and rotate it so that it is usable by pygame"""
        # fps + battery info
        self.fps = 1 / (time.time() - self.start)
        label = f'FPS: {self.fps :.1f} - BAT {battery}%'
        label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        cv2.rectangle(self.frame, (0, 0), (label_size[0] + self.margin, label_size[1] + base_line + self.margin),
                      color=(255, 255, 255), thickness=cv2.FILLED)
        cv2.putText(self.frame, label, (self.margin, label_size[1] + self.margin), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color=(0, 0, 0), thickness=1)

        # swapping
        self.frame = np.rot90(self.frame)
        self.out_frame = np.flipud(self.frame)
