class Baseline:
    def __init__(self, frames=[], max_frames=30, median_gray=None):
        self.frames = frames
        self.max_frames = max_frames
        self.median_gray = median_gray

    def append_frame(self, frame, force=False):
        if len(self.frames) >= self.max_frames:
            if not force:
                return False
        self.frames.append(frame)
        if len(self.frames) > self.max_frames:
            n_remove = len(self.frames) - self.max_frames
            del self.frames[0:n_remove]
