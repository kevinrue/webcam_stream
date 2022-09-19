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
    parser.add_argument("--blur_ksize")
    parser.add_argument("--threshold_min")
    parser.add_argument("--threshold_max")
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


def process_blur_ksize(ksize):
    # Parse string and convert to integer tuple
    ksize = tuple(int(x) for x in ksize.split("x"))
    return ksize


def process_threshold_min(threshold_min):
    threshold_min = int(threshold_min)
    return threshold_min


def process_threshold_max(threshold_max):
    threshold_max = int(threshold_max)
    return threshold_max
