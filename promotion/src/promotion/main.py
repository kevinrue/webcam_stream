import sys
from promotion.cli.args import (
    init_argparse,
    process_stream_input,
    process_integer,
    process_shape,
    process_margins,
    process_color)
from promotion.video.stream import App


def main():
    parser = init_argparse()
    args = parser.parse_args()
    filename = process_stream_input(args.filename)
    fps = process_integer(args.fps)
    resolution = process_shape(args.resolution)
    baseline_frequency = process_integer(args.baseline_frequency)
    baseline_frames = process_integer(args.baseline_frames)
    blur_ksize = process_shape(args.blur_ksize)
    threshold_min = process_integer(args.threshold_min)
    threshold_max = process_integer(args.threshold_max)
    detection_exclude_margins = process_margins(args.detection_exclude_margins)
    object_shape_min = process_shape(args.object_shape_min)
    object_rectangle_color = process_color(args.object_rectangle_color)
    object_rectangle_thickness = process_integer(args.object_rectangle_thickness)
    app = App(
        filename, fps, resolution, baseline_frames, baseline_frequency, blur_ksize, threshold_min,
        threshold_max, detection_exclude_margins, object_shape_min, object_rectangle_color, object_rectangle_thickness)
    app.open_stream()
    app.loop()


if __name__ == "__main__":
    sys.exit(main())
