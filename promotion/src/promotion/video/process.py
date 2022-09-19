import cv2


# Minimum object dimensions (height, width)
min_object_shape = (50, 50)
# Color of bounding rectangles around objects
bounding_rectangle_color = (0, 255, 0)
# Thickness of lines for bounding rectangles around objects
bounding_rectangle_thickness = 2


def process_frame(frame, baseline, blur_ksize, threshold_min, threshold_max):
    if baseline.median_gray_frame is None:
        return frame
    # Convert current frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate absolute difference of current frame and
    # the median frame
    difference_frame = cv2.absdiff(gray_frame, baseline.median_gray_frame)

    blurred = cv2.GaussianBlur(difference_frame, blur_ksize, 0)

    ret, tframe = cv2.threshold(
        blurred, threshold_min, threshold_max, cv2.THRESH_TOZERO
    )

    (cnts, _) = cv2.findContours(
        tframe.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if y > 200:  # Disregard item that are the top of the picture
            if h > min_object_shape[0] and w > min_object_shape[1]:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    bounding_rectangle_color,
                    bounding_rectangle_thickness,
                )

    return (frame)
