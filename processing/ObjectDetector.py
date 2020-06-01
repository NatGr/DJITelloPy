import cv2
import numpy as np
import os
from .FrameProcessor import FrameProcessor


class ObjectDetector(FrameProcessor):
    """Detects objects within a frame and annotates their position and confidence"""
    def __init__(self, model, input_size, threshold, nms, use_gpu):
        super().__init__()
        self.threshold, self.nms = threshold, nms
        classes = f"models/{model}/classes.txt"

        with open(classes) as file:
            self.classes = [name[:-1] for name in file.readlines()]  # removes the tailing \n
        np.random.seed(17)
        self.colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype="uint8")

        if "ssd" in model:
            cfg = f"models/{model}/model.pbtxt"
            weights = f"models/{model}/model.pb"
            self.net = cv2.dnn_DetectionModel(os.path.abspath(weights), os.path.abspath(cfg))
            self.net.setInputParams(size=(input_size, input_size), swapRB=False, crop=False,
                                    mean=127.5)  # mean is because of ssd preprocessing,
            # I should also have scale=2 / 255 but doing so fucks up the results...
        elif "yolo" in model:
            cfg = f"models/{model}/model.cfg"
            weights = f"models/{model}/model.weights"
            self.net = cv2.dnn_DetectionModel(os.path.abspath(weights), os.path.abspath(cfg))
            self.net.setInputParams(size=(input_size, input_size), swapRB=False, crop=False,
                                    scale=1 / 255.0)  # scale to go to the [0, 1] range
        else:
            raise ValueError("seems like there is a model name we can't handle")

        if use_gpu:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def process(self, frame: np.array, battery: int):
        """simply converts the color and disposition of the frame"""
        self.frame = frame
        super().preprocess_frame()

        out = self.net.detect(self.frame, self.threshold, self.nms)  # so that the time measurement is valid
        self.__draw_predictions(out)
        super().postprocess_frame(battery)

    def __draw_predictions(self, out):
        # Draw a bounding box for each prediction.
        for class_id, confidence, box in zip(*out):
            color = [int(c) for c in self.colors[class_id[0]]]
            left, top, right, bottom = box[0], box[1], box[0] + box[2], box[1] + box[3]
            cv2.rectangle(self.frame, (left, top), (right, bottom), color, thickness=2)
            label = f'{self.classes[class_id[0]]}: {confidence[0]: .2f}'
            label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            top = max(top, label_size[1])
            cv2.rectangle(self.frame, (left, top - label_size[1]), (left + label_size[0], top + base_line), color,
                          thickness=cv2.FILLED)
            cv2.putText(self.frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
