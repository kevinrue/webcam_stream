import sys
import cli.args
from video.stream import App


def main():
    parser = cli.args.init_argparse()
    args = parser.parse_args()
    filename = cli.args.process_stream_input(args.filename)
    fps = cli.args.process_integer(args.fps)
    resolution = cli.args.process_shape(args.resolution)
    baseline_frequency = cli.args.process_integer(args.baseline_frequency)
    baseline_frames = cli.args.process_integer(args.baseline_frames)
    blur_ksize = cli.args.process_shape(args.blur_ksize)
    threshold_min = cli.args.process_integer(args.threshold_min)
    threshold_max = cli.args.process_integer(args.threshold_max)
    object_shape_min = cli.args.process_shape(args.object_shape_min)
    object_rectangle_color = cli.args.process_color(args.object_rectangle_color)
    object_rectangle_thickness = cli.args.process_integer(args.object_rectangle_thickness)
    app = App(
        filename, fps, resolution, baseline_frames, baseline_frequency, blur_ksize, threshold_min,
        threshold_max, object_shape_min, object_rectangle_color, object_rectangle_thickness)
    app.open_stream()
    app.loop()
    


if __name__ == "__main__":
    sys.exit(main())
