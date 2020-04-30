import cv2
import numpy as np
from .FrameProcessor import FrameProcessor
import tflite_runtime.interpreter as tflite


class PoseDetector(FrameProcessor):
    """Detects persumn pose within a frame and annotates their position and mean confidence for all detected points.
    PoseNet postprocessing based on https://github.com/tensorflow/examples/blob/master/lite/examples/posenet/android/posenet/src/main/java/org/tensorflow/lite/examples/posenet/lib/Posenet.kt"""
    def __init__(self, model, threshold):
        super().__init__()
        self.threshold = threshold
        classes = f"models/{model}/classes.txt"

        with open(classes) as file:
            self.classes = [name[:-1] for name in file.readlines()]  # removes the tailing \n
        np.random.seed(17)
        self.colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype="uint8")

        self.interpreter = tflite.Interpreter(model_path=f"models/{model}/model.tflite")
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.input_shape = self.input_details[0]['shape']
        self.output_details = self.interpreter.get_output_details()

    def process(self, frame: np.array, battery: int):
        """simply converts the color and disposition of the frame"""
        self.frame = frame
        super().preprocess_frame()

        # pre-processing that open-cv handled for us and forward pass
        img = cv2.resize(self.frame, (self.input_shape[1], self.input_shape[2]))
        img = np.reshape(img, self.input_shape)
        img = (img.astype(np.float32) - 128.) / 128.  # standard scaling
        self.interpreter.set_tensor(self.input_details[0]['index'], img)
        self.interpreter.invoke()

        heatmaps = self.interpreter.get_tensor(self.output_details[0]['index'])[0]  # 1*9*9*17
        offsets = self.interpreter.get_tensor(self.output_details[1]['index'])[0]  # 1*9*9*34

        # replacing heatmaps by their softmax
        heatmaps = np.exp(heatmaps)
        heatmaps = heatmaps / heatmaps.sum(axis=(0, 1))

        # getting x, y coordinates for each points
        max_rows, max_cols = np.unravel_index(np.argmax(heatmaps.reshape((-1, heatmaps.shape[2])), axis=0),
                                              shape=heatmaps.shape[:2])  # flatten the array,
        # get argmax and reconvert the indexes
        kpt_y = (max_rows / (heatmaps.shape[0] - 1) + offsets[max_rows, max_cols, np.arange(heatmaps.shape[2])] /
                 self.input_shape[1]) * self.frame.shape[0]
        kpt_x = self.frame.shape[1] * (max_cols / (heatmaps.shape[1] - 1) +
                 offsets[max_rows, max_cols, np.arange(heatmaps.shape[2], 2 * heatmaps.shape[2])] / self.input_shape[2])

        # show points above threshold
        index_to_keep = np.argwhere(heatmaps[max_rows, max_cols, np.arange(heatmaps.shape[2])] > self.threshold)

        self.__draw_predictions(kpt_x, kpt_y, index_to_keep)
        super().postprocess_frame(battery)

    def __draw_predictions(self, kpt_x, kpt_y, index_to_keep):
        # Draw a point for each prediction.
        for i in index_to_keep:
            cv2.circle(self.frame, (kpt_x[i], kpt_y[i]), radius=10, color=[int(j) for j in self.colors[i][0]],
                       thickness=-1)
