import cv2
import numpy as np
import os
from .FrameProcessor import FrameProcessor


class ObjectSegmentor(FrameProcessor):
    """Segments objects within a frame and annotates their position and confidence. This class uses MaskRCNN"""
    def __init__(self, input_size, threshold, mask_threshold, use_gpu):
        super().__init__()
        self.threshold, self.mask_threshold = threshold, mask_threshold
        classes = "models/maskrcnn/classes.txt"
        cfg = f"models/maskrcnn/model.pbtxt"
        weights = f"models/maskrcnn/model.pb"

        with open(classes) as file:
            self.classes = [name[:-1] for name in file.readlines()]  # removes the tailing \n
        np.random.seed(17)
        self.colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype="uint8")
        self.net = cv2.dnn.readNetFromTensorflow(os.path.abspath(weights), os.path.abspath(cfg))
        self.input_size = input_size

        if use_gpu:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def process(self, frame: np.array, battery: int):
        """simply converts the color and disposition of the frame"""
        self.frame = frame
        super().preprocess_frame()

        resized = cv2.resize(self.frame, (self.input_size, self.input_size), interpolation=cv2.INTER_NEAREST)
        blob = cv2.dnn.blobFromImage(resized, swapRB=True, crop=False)
        self.net.setInput(blob)
        boxes, masks = self.net.forward(["detection_out_final", "detection_masks"])

        self.__draw_predictions(boxes, masks)
        super().postprocess_frame(battery)

    def __draw_predictions(self, boxes, masks):
        # Draw a segmentation mask for each prediction above threshold.
        height, width = self.frame.shape[:2]
        bb_scaler = np.array([width, height, width, height])

        for i in range(0, boxes.shape[2]):
            class_id = int(boxes[0, 0, i, 1])
            confidence = boxes[0, 0, i, 2]
            if confidence > self.threshold:  # filter out preds with weak confidence

                # scale bounding boxes
                box = boxes[0, 0, i, 3:7] * bb_scaler
                start_x, start_y, end_x, end_y = box.astype("int")
                box_w, box_h = end_x - start_x, end_y - start_y

                # get binary mask
                mask = masks[i, class_id]
                mask = cv2.resize(mask, (box_w, box_h), interpolation=cv2.INTER_NEAREST)
                mask = mask > self.mask_threshold

                # draw segmentation mask on frame
                color = self.colors[class_id]

                segmented_object = ((0.4 * color) +
                                    (0.6 * self.frame[start_y:end_y, start_x:end_x][mask])).astype("uint8")
                self.frame[start_y:end_y, start_x:end_x][mask] = segmented_object

                # draw label on frame
                color = [int(c) for c in color]
                label = f'{self.classes[class_id]}: {confidence: .2f}'
                label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                start_y = max(start_y, label_size[1])
                cv2.rectangle(self.frame, (start_x, start_y - label_size[1]),
                              (start_x + label_size[0], start_y + base_line), color, thickness=cv2.FILLED)
                cv2.putText(self.frame, label, (start_x, start_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
