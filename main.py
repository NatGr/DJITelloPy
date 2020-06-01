import argparse
import sys
from FrontEnd import FrontEnd
from processing import FrameProcessor, ObjectDetector, PoseDetector


# prints to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("""Controls a dji tello edu drone""")
    parser.add_argument("--drone_speed", help="speed of the drone in cm/s, must be within [10, 100]", type=int,
                        default=60)
    parser.add_argument("--azerty", action="store_true",
                        help="use qzsd instead of asdw for left-hand control (better for an azerty keyboard)")
    parser.add_argument("--model", help="which model to use. None for default video stream, "
                                        "{yolo|ssd}.* for object recognition, "
                                        "posenet for pose detection (limited to a single person)", type=str,
                        choices=["None", "yolov3", "yolov3_tiny", "ssd_mobv1", "ssd_mobv2", "posenet"],
                        default="yolov3")
    parser.add_argument("--threshold", type=float, default=.5,
                        help="threshold under which predictions are ignored (ignored when --model is None)")
    parser.add_argument("--nms", help="IOU threshold used in non maximum supression (ignored when not doing object "
                                      "detection)", type=float, default=.3)
    parser.add_argument("--input_size", type=int, default=320,
                        help="size to which the image is resized before being fed to a network. We recommend 320 for"
                             "yolov3, 416 for yolov3_tiny, 300 for the ssds, input size is always 257 for posenet")
    parser.add_argument("--use_gpu", action="store_true",
                        help="Set to true if you want to use gpu instead of cpu to perform inference, will have no "
                             "effect if model is None or posenet")
    parser.add_argument("--video_name", default="", type=str,
                        help="If not empty, name of the file where video will be recorded, otherwise the video is not "
                             "saved on disk")

    args = parser.parse_args()
    if args.drone_speed < 10 or args.drone_speed > 100:
        eprint("speed of the drone in cm/s must be within [10, 100]")
        exit(1)
    if args.threshold < 0 or args.threshold >= 1:
        eprint("the threshold must be within [0, 1[")
        exit(1)
    if args.nms < 0 or args.nms >= 1:
        eprint("the nms must be within [0, 1[")
        exit(1)
    if args.input_size < 224 or args.input_size > 720:
        eprint("As input image is 960*720 and 224 is quite small, input size must be within [224, 720]")
        exit(1)

    if args.model == "None":
        frame_processor = FrameProcessor()
    elif args.model.startswith("yolo") or args.model.startswith("ssd"):
        frame_processor = ObjectDetector(args.model, args.input_size, args.threshold, args.nms, args.use_gpu)
    elif args.model == "posenet":
        frame_processor = PoseDetector(args.model, args.threshold)
    else:
        raise ValueError("Not implemented")

    frontend = FrontEnd(args.drone_speed, args.azerty, frame_processor, args.video_name)
    frontend.run()
