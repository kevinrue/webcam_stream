import cv2
from video.baseline import Baseline
from video.process import process_frame


def get_stream(filename):
    video_stream = cv2.VideoCapture(filename)
    if not video_stream.isOpened():
        raise IOError("Cannot open video stream")
    return video_stream


def loop_stream(
    video_stream, fps, ksize, threshold_min, threshold_max, object_shape_min, object_rectangle_color,
    object_rectangle_thickness
):
    baseline = Baseline(fps=fps)
    ret, frame = video_stream.read()
    while ret and frame.shape[0] > 0 and frame.shape[1] > 0:

        baseline.append_frame(frame)
        baseline.compute_median_gray()
        frame = process_frame(
            frame, baseline, ksize, threshold_min, threshold_max, object_shape_min, object_rectangle_color,
            object_rectangle_thickness)

        # Display
        cv2.imshow("Output", frame)
        # Duration of each frame on screen
        c = cv2.waitKey(int(1000 / fps))
        if c == 27:
            break

        # Read next frame
        ret, frame = video_stream.read()
