import argparse
import sys
import cli.args
from video.stream import get_stream, loop_stream


def main():
    parser = init_argparse()
    args = parser.parse_args()
    filename = cli.args.process_filename(args.filename)
    fps = cli.args.process_fps(args.fps)
    video_stream = get_stream(filename)
    loop_stream(video_stream, fps)
    video_stream.release()


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Print or check SHA1 (160-bit) checksums.",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument("-f", "--filename")
    parser.add_argument("--fps")
    return parser


if __name__ == "__main__":
    sys.exit(main())
