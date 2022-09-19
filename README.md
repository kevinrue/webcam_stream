## Overview

This repsitory contains a number of different attempts at processing
a webcam feed or recorded video for the purpose of motion detection
and home security.

## Contents

### 01-webapp

A `flask` light web application serving the stream of a webcam on a localhost webpage.

### 02-opencv-tutorial

Naive adaptation of a tutorial to the stream of a webcam.

The webcam was streaming the view of a street with passing cars and pedestrians.

The objective was to detect both cars and pedestrians.

### 03-opencv-street-ipynb

Use of the same tutorial as `02-opencv-tutorial` to optimise parameters for a recorded video.

The video recorded the view of a street with passing cars and pedestrians.

The objective was to detect both cars and pedestrians.

### 04-opencv-street-py

Use of the optimised parameters in `03-opencv-street-ipynb`
and major modifications to the app in `02-opencv-tutorial`
to simultaneously display frames at key steps of processing.

### promotion

Python package that collates the scripts above.

#### Usage

```bash
python promotion/src/promotion/main.py \
    -f 1 \
    --fps 10 \
    --resolution 960x540 \
    --blur_ksize 61x61 \
    --threshold_min 5 \
    --threshold_max 255 \
    --object_shape_min 50x50 \
    --object_rectangle_color 0:255:0 \
    --object_rectangle_thickness 2
```
