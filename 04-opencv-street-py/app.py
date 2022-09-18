import numpy as np
import cv2

##
# Static variables (parameters)
##

# Number of control frames
n_control_frames = 10
# Sample rate for control images (i.e., use 1 frame every X frames)
sample_rate_control = 10
# Skip frames during detection
n_frames_skip_detection = 0
# Gaussian blurring kernel size
blurring_gaussian_kernel_size = (61, 61)
# Minimum object dimensions (height, width)
min_object_shape = (75, 75)
# Color of bounding rectangles around objects
bounding_rectangle_color = (0, 255, 0)
# Thickness of lines for bounding rectangles around objects
bounding_rectangle_thickness = 2
# Threshold on the minimum intensity (lower values are set to 0)
threshold_min = 5
# Threshold on the maximum intensity (higher values are capped)
threshold_max = 255

##
# Variables changing over time
##

# List of frames used to compute the control frame
control_frames = []
# Control frame
gray_median_frame = None
# Frame counter
n_frames_streamed = 0

video_stream = cv2.VideoCapture("videos/office.mp4")
# Check if the webcam is opened correctly
if not video_stream.isOpened():
    raise IOError("Cannot open file")

ret, frame = video_stream.read()
while ret and frame.shape[0] > 0 and frame.shape[1] > 0:
    n_frames_streamed += 1
    # TODO: sample frames over time
    # - update to account for change in daylight
    # - discard and replace outlier frames (e.g., that contain objects)
    if len(control_frames) < n_control_frames:
        if n_frames_streamed % sample_rate_control == 0:
            control_frames.append(frame)

    if len(control_frames) == n_control_frames and gray_median_frame is None:
        # Calculate the median along the time axis
        median_frame = np.median(control_frames, axis=0).astype(dtype=np.uint8)
        # Convert median frame to gray
        gray_median_frame = cv2.cvtColor(median_frame, cv2.COLOR_BGR2GRAY)

    if n_frames_streamed <= n_frames_skip_detection or gray_median_frame is None:
        ret, frame = video_stream.read()
        continue

    # Convert current frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate absolute difference of current frame and
    # the median frame
    difference_frame = cv2.absdiff(gray_frame, gray_median_frame)

    blurred = cv2.GaussianBlur(
        difference_frame, blurring_gaussian_kernel_size, 0)

    ret, tframe = cv2.threshold(
        blurred, threshold_min, threshold_max, cv2.THRESH_TOZERO)

    (cnts, _) = cv2.findContours(
        tframe.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if y > 200:  # Disregard item that are the top of the picture
            if h > min_object_shape[0] or h > min_object_shape[1]:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    bounding_rectangle_color,
                    bounding_rectangle_thickness,
                )
                cv2.rectangle(
                    gray_frame,
                    (x, y),
                    (x + w, y + h),
                    (255, 255, 255),
                    bounding_rectangle_thickness,
                )
                cv2.rectangle(
                    difference_frame,
                    (x, y),
                    (x + w, y + h),
                    (255, 255, 255),
                    bounding_rectangle_thickness,
                )
                cv2.rectangle(
                    tframe,
                    (x, y),
                    (x + w, y + h),
                    (255, 255, 255),
                    bounding_rectangle_thickness,
                )

    cv2.putText(frame, "Native frame", (1920-250, 1080-30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(gray_frame, "Gray frame", (1920-450, 1080-30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(tframe, "Thresholded frame", (1920-350, 1080-30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(gray_median_frame, "Gray median frame", (1920-550, 1080-30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    stacked_frames = np.vstack((
        np.hstack((
            frame,
            cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
        )),
        np.hstack((
            cv2.cvtColor(tframe, cv2.COLOR_GRAY2BGR),
            cv2.cvtColor(gray_median_frame, cv2.COLOR_GRAY2BGR)
        ))
    ))

    # Display
    cv2.imshow("Output", stacked_frames)
    c = cv2.waitKey(1)
    if c == 27:
        break

    # Read next frame
    ret, frame = video_stream.read()

video_stream.release()
