import cv2
from video.baseline import Baseline


def get_stream(filename):
    video_stream = cv2.VideoCapture(filename)
    if not video_stream.isOpened():
        raise IOError("Cannot open video stream")
    return video_stream


def loop_stream(video_stream):
    baseline = Baseline()
    ret, frame = video_stream.read()
    while ret and frame.shape[0] > 0 and frame.shape[1] > 0:

        baseline.append_frame(frame)
        baseline.compute_median_gray()

        # Display
        cv2.imshow("Output", frame)
        c = cv2.waitKey(1)
        if c == 27:
            break

        # Read next frame
        ret, frame = video_stream.read()
