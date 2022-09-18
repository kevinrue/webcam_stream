def process_filename(filename):
    if filename.isdigit():
        filename = int(filename)
    else:
        filename = filename
    return filename

def process_fps(fps):
    fps = int(fps)
    return fps
