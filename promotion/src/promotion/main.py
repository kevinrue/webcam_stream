import argparse
import cv2
import sys
from cli.args import process_filename
from video.stream import get_stream


def main():
    parser = init_argparse()
    args = parser.parse_args()
    filename = process_filename(args.filename)
    video_stream = get_stream(filename)

    ret, frame = video_stream.read()
    while ret and frame.shape[0] > 0 and frame.shape[1] > 0:

        # Display
        cv2.imshow("Output", frame)
        c = cv2.waitKey(1)
        if c == 27:
            break

        # Read next frame
        ret, frame = video_stream.read()

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
    parser.add_argument("files", nargs="*")
    return parser


if __name__ == "__main__":
    sys.exit(main())
