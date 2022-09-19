import cv2
import datetime
import numpy as np


class Baseline:
    def __init__(self, frames=[], max_frames=30, median_gray=None, fps=30):
        self.frames = frames
        self.max_frames = max_frames
        self.median_gray_frame = median_gray
        self.timedelta_min_seconds = 1 / fps
        self.latest_update = datetime.datetime.now()

    def append_frame(self, frame, force=False):
        now = datetime.datetime.now()
        time_since_latest = now - self.latest_update
        if len(self.frames) >= self.max_frames or time_since_latest.total_seconds() < self.timedelta_min_seconds:
            if not force:
                return False
        self.frames.append(frame)
        self.latest_update = now
        if len(self.frames) > self.max_frames:
            n_remove = len(self.frames) - self.max_frames
            del self.frames[0:n_remove]

    def compute_median_gray(self, force=False):
        if len(self.frames) < self.max_frames or self.median_gray_frame is not None:
            if not force:
                return False
        # Calculate the median along the time axis
        median_frame = np.median(self.frames, axis=0).astype(dtype=np.uint8)
        # Convert median frame to gray
        self.median_gray_frame = cv2.cvtColor(median_frame, cv2.COLOR_BGR2GRAY)
