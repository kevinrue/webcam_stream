import argparse


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


def process_filename(filename):
    if filename.isdigit():
        filename = int(filename)
    else:
        filename = filename
    return filename


def process_fps(fps):
    fps = int(fps)
    return fps
