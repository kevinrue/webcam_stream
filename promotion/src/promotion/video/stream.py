import cv2

def get_stream(filename):
    video_stream = cv2.VideoCapture(filename)
    if not video_stream.isOpened():
        raise IOError("Cannot open video stream")
    return(video_stream)
