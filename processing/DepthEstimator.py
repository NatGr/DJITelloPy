import cv2
import numpy as np
import os
from .FrameProcessor import FrameProcessor


class DepthEstimator(FrameProcessor):
    """estimates depth within a frame and annotates their position and confidence. This class uses the midas model"""
    def __init__(self, input_size, use_gpu):
        super().__init__()
        self.input_size = input_size
        self.scale_min = 20000
        self.scale_range = 80000 / 255  # / 255 because we need an uint8 range

        self.net = cv2.dnn.readNetFromONNX(os.path.abspath("models/midas/model.onnx"))  # includes input pixels scaling

        if use_gpu:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def process(self, frame: np.array, battery: int):
        """simply converts the color and disposition of the frame"""
        self.frame = frame
        height, width = self.frame.shape[:2]
        super().preprocess_frame()

        resized = cv2.resize(self.frame, (self.input_size, self.input_size), interpolation=cv2.INTER_NEAREST)
        blob = cv2.dnn.blobFromImage(resized, swapRB=True, crop=False)
        self.net.setInput(blob)

        # transpose, normalize, resize and colors the predicted output
        depth_map = self.net.forward(["1195"])[0].transpose((1, 2, 0))
        depth_map = ((depth_map - self.scale_min) / self.scale_range).astype("uint8")
        depth_map = cv2.resize(depth_map, (width, height), interpolation=cv2.INTER_NEAREST)
        self.frame = cv2.applyColorMap(depth_map, cv2.COLORMAP_JET)

        super().postprocess_frame(battery)


