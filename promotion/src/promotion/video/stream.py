import cv2
from video.baseline import Baseline


class App:
    def __init__(
        self, filename, fps, resolution, baseline_frames, baseline_frequency, blur_ksize, threshold_min,
        threshold_max, detection_exclude_margins, object_shape_min, object_rectangle_color, object_rectangle_thickness
    ):
        self.filename = filename
        self.fps = fps
        self.blur_ksize = blur_ksize
        self.threshold_min = threshold_min
        self.threshold_max = threshold_max
        self.detection_exclude_margins = detection_exclude_margins
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
            frame = self.process_frame(frame)

            # Display
            cv2.imshow("Output", frame)
            # Duration of each frame on screen
            c = cv2.waitKey(int(1000 / self.fps))
            if c == 27:
                break

            # Read next frame
            ret, frame = self.stream.read()
    
    def process_frame(self, frame):
        if self.baseline.median_gray_frame is None:
            return frame
        if self.baseline.resolution is not None:
            frame = cv2.resize(frame, (self.baseline.resolution[0], self.baseline.resolution[1]))
        # Convert current frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate absolute difference of current frame and the median frame
        difference_frame = cv2.absdiff(gray_frame, self.baseline.median_gray_frame)
        # Apply Gaussian blur to smooth the frame of absolute differences
        blurred = cv2.GaussianBlur(difference_frame, self.blur_ksize, 0)
        # Apply threshold(s) to the smoothed difference
        ret, tframe = cv2.threshold(
            blurred, self.threshold_min, self.threshold_max, cv2.THRESH_TOZERO
        )
        # Find contours in the thresholded difference
        (cnts, _) = cv2.findContours(
            tframe.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        # Draw contours on the current frame
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            if y > self.detection_exclude_margins[0]:
                if h > self.object_shape_min[0] and w > self.object_shape_min[1]:
                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        self.object_rectangle_color,
                        self.object_rectangle_thickness,
                    )

        return (frame)