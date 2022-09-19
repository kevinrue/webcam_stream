import argparse
from ast import parse


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
    parser.add_argument("--resolution")
    parser.add_argument("--blur_ksize")
    parser.add_argument("--threshold_min")
    parser.add_argument("--threshold_max")
    parser.add_argument("--object_shape_min")
    parser.add_argument("--object_rectangle_color")
    parser.add_argument("--object_rectangle_thickness")
    return parser


def process_stream_input(filename):
    if filename.isdigit():
        value = int(filename)
    else:
        value = filename
    return value


def process_integer(fps):
    value = int(fps)
    return value


def process_shape(string):
    # Parse string and convert to integer tuple
    value = tuple(int(x) for x in string.split("x"))
    return value


def process_color(string):
    # Parse string and convert to integer tuple
    value = tuple(int(x) for x in string.split(":"))
    return value
