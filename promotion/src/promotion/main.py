import argparse
import cv2
import sys


def args_process_filename(filename):
    if filename.isdigit():
        filename = int(filename)
    else:
        filename = filename
    return filename


def main():
    parser = init_argparse()
    args = parser.parse_args()
    filename = args_process_filename(args.filename)
    video_stream = cv2.VideoCapture(filename)
    if not video_stream.isOpened():
        raise IOError("Cannot open video stream")

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
