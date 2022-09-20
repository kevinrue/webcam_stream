import cv2


def process_frame(
    frame, baseline, blur_ksize, threshold_min, threshold_max, detection_exclude_margins,
    object_shape_min, object_rectangle_color, object_rectangle_thickness
):
    if baseline.median_gray_frame is None:
        return frame
    if baseline.resolution is not None:
        frame = cv2.resize(frame, (baseline.resolution[0], baseline.resolution[1]))
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
        if y > detection_exclude_margins[0]:
            if h > object_shape_min[0] and w > object_shape_min[1]:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    object_rectangle_color,
                    object_rectangle_thickness,
                )

    return (frame)
