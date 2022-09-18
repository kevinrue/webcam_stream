import cv2
import sys


def main(filename=0):
    video_stream = cv2.VideoCapture(filename)
    if not video_stream.isOpened():
        raise IOError("Cannot open video stream")
    video_stream.release()


if __name__ == "__main__":
    sys.exit(main())
