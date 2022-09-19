import sys
import cli.args
from video.stream import get_stream, loop_stream


def main():
    parser = cli.args.init_argparse()
    args = parser.parse_args()
    filename = cli.args.process_filename(args.filename)
    fps = cli.args.process_fps(args.fps)
    ksize = cli.args.process_blur_ksize(args.blur_ksize)
    threshold_min = cli.args.process_threshold_min(args.threshold_min)
    threshold_max = cli.args.process_threshold_max(args.threshold_max)
    video_stream = get_stream(filename)
    loop_stream(video_stream, fps, ksize, threshold_min, threshold_max)
    video_stream.release()


if __name__ == "__main__":
    sys.exit(main())
