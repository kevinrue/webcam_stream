import numpy as np
import cv2
import random
from matplotlib import pyplot as plt

n_control_frames = 10
control_frames = []
grayMedianFrame = False

video_stream = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not video_stream.isOpened():
    raise IOError("Cannot open webcam")

while True:
    # Read captured image
    ret, frame = video_stream.read()

    # resize image
    frame = cv2.resize(frame, (960, 540))

    if len(control_frames) < n_control_frames:
        if random.random() < 0.1:
            control_frames.append(frame)
            print(
                f"{len(control_frames)} of {n_control_frames} control images collected."
            )
        # tframe = frame.copy()
    else:
        # Calculate the median along the time axis
        medianFrame = np.median(control_frames, axis=0).astype(dtype=np.uint8)
        # plt.imshow(fixColor(medianFrame))

        # Convert median frame to gray
        grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)
        # plt.imshow(fixColor(grayMedianFrame))
        # cv2.imwrite("grayMedianFrame.jpg", grayMedianFrame)
        # Convert current frame to grayscale
        gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate absolute difference of current frame and
        # the median frame
        dframe = cv2.absdiff(gframe, grayMedianFrame)
        # Gaussian
        blurred = cv2.GaussianBlur(dframe, (11, 11), 0)
        # Thresholding to binarise
        ret, tframe = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)
        # Identifying contours from the threshold
        (cnts, _) = cv2.findContours(
            tframe.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        print(len(cnts))
        # For each contour draw the bounding box
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            if y > 200:  # Disregard items in the top of the picture
                # if w > 100 and h > 100:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

    # Display
    cv2.imshow("Input", frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

video_stream.release()
cv2.destroyAllWindows()

# python3 -m http.server
