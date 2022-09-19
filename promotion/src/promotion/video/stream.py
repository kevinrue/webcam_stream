import cv2
from video.baseline import Baseline
from video.process import process_frame


class App:
    def __init__(
        self, filename, fps, resolution, baseline_frames, baseline_frequency, blur_ksize, threshold_min,
        threshold_max, object_shape_min, object_rectangle_color, object_rectangle_thickness
    ):
        self.filename = filename
        self.fps = fps
        self.blur_ksize = blur_ksize
        self.threshold_min = threshold_min
        self.threshold_max = threshold_max
        self.object_shape_min = object_shape_min
        self.object_rectangle_color = object_rectangle_color
        self.object_rectangle_thickness = object_rectangle_thickness
        self.baseline = Baseline(resolution=resolution, max_frames=baseline_frames, frequency=baseline_frequency)
        self.stream = None

    def open_stream(self):
        self.stream = cv2.VideoCapture(self.filename)
        if not self.stream.isOpened():
            raise IOError("Cannot open video stream")
    
    def release_stream(self):
        self.stream.release()

    def loop(self):
        ret, frame = self.stream.read()
        while ret and frame.shape[0] > 0 and frame.shape[1] > 0:

            self.baseline.append_frame(frame)
            self.baseline.compute_median_gray()
            frame = process_frame(
                frame, self.baseline, self.blur_ksize, self.threshold_min, self.threshold_max, self.object_shape_min,
                self.object_rectangle_color, self.object_rectangle_thickness)

            # Display
            cv2.imshow("Output", frame)
            # Duration of each frame on screen
            c = cv2.waitKey(int(1000 / self.fps))
            if c == 27:
                break

            # Read next frame
            ret, frame = self.stream.read()
